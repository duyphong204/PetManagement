import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
import mysql.connector
import pickle
import faiss

# Khởi tạo biến toàn cục
model = None
feature_model = None
db = None
cursor = None
faiss_index = None
pet_info = None

def initialize_model_and_db():
    global model, feature_model, db, cursor, faiss_index, pet_info
    try:
        # Tải mô hình phân loại
        if model is None:
            model = tf.keras.models.load_model("models/pet_recognition_model.keras")
        
        # Tải mô hình VGG16 để trích xuất đặc trưng
        if feature_model is None:
            base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
            feature_model = tf.keras.Sequential([base_model, tf.keras.layers.GlobalAveragePooling2D()])

        # Kết nối CSDL và xây dựng Faiss index
        if db is None or cursor is None:
            db = mysql.connector.connect(host="localhost", user="root", password="", database="qlthucung1")
            cursor = db.cursor()
            cursor.execute("SELECT id, ten_thu_cung, id_chu_so_huu, loai, feature_vector FROM thu_cung_metadata")
            rows = cursor.fetchall()

            features, pet_info = [], []
            for row in rows:
                pet_id, ten_thu_cung, id_chu_so_huu, loai, feature_blob = row
                if feature_blob:
                    feature = pickle.loads(feature_blob)
                    features.append(feature)
                    pet_info.append((pet_id, ten_thu_cung, id_chu_so_huu, loai))

            if not features:
                return False
            features = np.array(features, dtype=np.float32)
            faiss_index = faiss.IndexFlatL2(features.shape[1])
            faiss_index.add(features)
        return True
    except Exception as e:
        print(f"Khởi tạo thất bại: {e}")
        return False

def recognize_pet_from_image(img):
    global model, cursor, faiss_index, pet_info
    # Phân loại Dog/Cat
    img_resized = cv2.resize(img, (224, 224)) / 255.0
    prediction = model.predict(np.expand_dims(img_resized, axis=0))
    confidence = float(prediction[0]) if prediction[0] > 0.5 else 1.0 - float(prediction[0])
    label = "Dog" if prediction[0] > 0.5 else "Cat"

    # Trích xuất đặc trưng
    img_rgb = cv2.cvtColor(cv2.resize(img, (224, 224)), cv2.COLOR_BGR2RGB)
    img_preprocessed = preprocess_input(np.expand_dims(img_rgb, axis=0))
    input_feature = feature_model.predict(img_preprocessed).flatten()
    if input_feature is None:
        return label, f"{label}", "Lỗi trích xuất đặc trưng", confidence, float('inf'), "Không có thông tin lịch hẹn"

    # Tìm bản ghi khớp bằng Faiss
    distances, indices = faiss_index.search(np.array([input_feature], dtype=np.float32), k=1)
    min_distance, best_match_idx = distances[0][0], indices[0][0]

    threshold = 1.0
    if min_distance < threshold:
        pet_id, ten_thu_cung, id_chu_so_huu, pet_loai = pet_info[best_match_idx]
        if pet_loai.lower() != label.lower():
            return label, f"{label}", "Không có thông tin về thú cưng này", confidence, min_distance, "Không có thông tin lịch hẹn"

        # Truy vấn thông tin chủ
        cursor.execute("SELECT ten_chu FROM chu_so_huu WHERE id = %s", (id_chu_so_huu,))
        owner_name = cursor.fetchone()[0] if cursor.fetchone() else "Không có thông tin chủ"

        # Truy vấn lịch hẹn
        cursor.execute(
            "SELECT ngay_hen, gio_hen, trang_thai FROM lich_hen WHERE id_thu_cung = %s AND trang_thai = 'approved' ORDER BY ngay_hen DESC LIMIT 1",
            (pet_id,)
        )
        appointment = cursor.fetchone()
        appointment_info = f"Lịch hẹn: {appointment[0]} {appointment[1]} ({appointment[2]})" if appointment else "Không có lịch hẹn"
    else:
        ten_thu_cung = f"{label}"
        owner_name = "Không có thông tin về thú cưng này"
        appointment_info = "Không có thông tin lịch hẹn"

    return label, ten_thu_cung, owner_name, confidence, min_distance, appointment_info

def get_webcam_frame(cap):
    ret, frame = cap.read()
    return frame if ret else None