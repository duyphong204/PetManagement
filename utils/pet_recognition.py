# utils/pet_recognition.py
try:
    import cv2
    import numpy as np
    import tensorflow as tf
    from tensorflow.keras.applications import VGG16
    from tensorflow.keras.applications.vgg16 import preprocess_input
    from tensorflow.keras.models import Model
    import mysql.connector
    import pickle
    import faiss
except ImportError as e:
    print(f"Lỗi: Thiếu thư viện - {e}")
    print("Hãy cài đặt các thư viện cần thiết bằng lệnh:")
    print("pip install opencv-python tensorflow numpy mysql-connector-python faiss-cpu")
    exit(1)

# Không tải mô hình và kết nối MySQL ngay từ đầu
model = None
feature_model = None
db = None
cursor = None
faiss_index = None
pet_info = None

def initialize_model_and_db():
    global model, feature_model, db, cursor, faiss_index, pet_info
    # Tải mô hình phân loại Dog/Cat
    if model is None:
        try:
            model = tf.keras.models.load_model("models/pet_recognition_model.keras")
        except Exception as e:
            print(f"Lỗi khi tải mô hình: {e}")
            print("Hãy đảm bảo file 'models/pet_recognition_model.keras' đã tồn tại.")
            print("Chạy file 'utils/train_model.py' để huấn luyện và tạo mô hình.")
            return False

    # Tải mô hình trích xuất đặc trưng (VGG16)
    if feature_model is None:
        base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        feature_model = tf.keras.Sequential([
            base_model,
            tf.keras.layers.GlobalAveragePooling2D()
        ])

    # Kết nối MySQL và xây dựng Faiss index
    if db is None or cursor is None:
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Thay bằng mật khẩu của bạn nếu có
                database="qlthucung1"
            )
            cursor = db.cursor()

            # Lấy tất cả đặc trưng từ CSDL để xây dựng Faiss index
            cursor.execute("SELECT id, ten_thu_cung, id_chu_so_huu, loai, feature_vector FROM thu_cung_metadata")
            rows = cursor.fetchall()

            # Chuẩn bị dữ liệu cho Faiss
            features = []
            pet_info = []
            for row in rows:
                pet_id, ten_thu_cung, id_chu_so_huu, loai, feature_blob = row
                if feature_blob is None:
                    print(f"Bản ghi ID {pet_id} không có dữ liệu đặc trưng")
                    continue
                try:
                    feature = pickle.loads(feature_blob)
                    features.append(feature)
                    pet_info.append((pet_id, ten_thu_cung, id_chu_so_huu, loai))
                except Exception as e:
                    print(f"Lỗi khi giải mã đặc trưng của bản ghi ID {pet_id}: {e}")
                    continue

            if not features:
                print("Không có đặc trưng nào để xây dựng Faiss index")
                return False

            # Xây dựng Faiss index
            features = np.array(features, dtype=np.float32)
            dimension = features.shape[1]
            faiss_index = faiss.IndexFlatL2(dimension)
            faiss_index.add(features)
            print(f"Đã xây dựng Faiss index với {faiss_index.ntotal} đặc trưng")
        except mysql.connector.Error as e:
            print(f"Lỗi khi kết nối CSDL: {e}")
            print("Hãy kiểm tra thông tin kết nối MySQL (host, user, password, database).")
            return False
    return True

def extract_feature(img):
    try:
        # Tiền xử lý ảnh
        img = cv2.resize(img, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        # Trích xuất đặc trưng
        feature = feature_model.predict(img)
        return feature.flatten()
    except Exception as e:
        print(f"Lỗi khi trích xuất đặc trưng: {e}")
        return None

def recognize_pet_from_image(img):
    global model, cursor, faiss_index, pet_info
    # Tiền xử lý ảnh để phân loại Dog/Cat
    img_resized = cv2.resize(img, (224, 224)) / 255.0
    img_expanded = np.expand_dims(img_resized, axis=0)

    # Dự đoán loại (Dog hoặc Cat)
    prediction = model.predict(img_expanded)
    confidence = float(prediction[0]) if prediction[0] > 0.5 else 1.0 - float(prediction[0])
    label = "Dog" if prediction[0] > 0.5 else "Cat"
    print(f"Dự đoán loại: {label} (Confidence: {confidence:.2f})")

    # Trích xuất đặc trưng của ảnh đầu vào
    input_feature = extract_feature(img)
    if input_feature is None:
        print("Không thể trích xuất đặc trưng ảnh đầu vào")
        return label, f"{label}", "Lỗi khi trích xuất đặc trưng ảnh đầu vào", confidence, float('inf')

    # Sử dụng Faiss để tìm bản ghi khớp
    try:
        input_feature = np.array([input_feature], dtype=np.float32)
        distances, indices = faiss_index.search(input_feature, k=1)
        min_distance = distances[0][0]
        best_match_idx = indices[0][0]
        print(f"Khoảng cách nhỏ nhất (L2 distance): {min_distance:.4f}")

        threshold = 1.0  # Tăng ngưỡng để dễ khớp hơn (có thể điều chỉnh)
        if min_distance < threshold:
            pet_id, ten_thu_cung, id_chu_so_huu, pet_loai = pet_info[best_match_idx]
            print(f"Bản ghi khớp: ID={pet_id}, Tên thú cưng={ten_thu_cung}, Loại={pet_loai}")
            # Kiểm tra xem loai có khớp không
            if pet_loai.lower() != label.lower():
                print("Loại không khớp với dự đoán")
                return label, f"{label}", "Không có thông tin về thú cưng này trong hệ thống", confidence, min_distance
            # Truy vấn tên chủ từ bảng chu_so_huu
            if id_chu_so_huu:
                cursor.execute("SELECT ten_chu FROM chu_so_huu WHERE id = %s", (id_chu_so_huu,))
                owner_result = cursor.fetchone()
                owner_name = owner_result[0] if owner_result else "Không có thông tin chủ trong hệ thống"
            else:
                owner_name = "Không có thông tin chủ trong hệ thống"
        else:
            print("Khoảng cách vượt quá ngưỡng, không tìm thấy bản ghi khớp")
            ten_thu_cung = f"{label}"
            owner_name = "Không có thông tin về thú cưng này trong hệ thống"
    except Exception as e:
        print(f"Lỗi khi so sánh đặc trưng: {e}")
        ten_thu_cung = f"{label}"
        owner_name = "Lỗi khi so sánh đặc trưng"
        min_distance = float('inf')

    return label, ten_thu_cung, owner_name, confidence, min_distance

def get_webcam_frame(cap):
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc frame từ webcam.")
        return None
    return frame