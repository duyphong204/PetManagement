# utils/extract_features.py
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.models import Model
import mysql.connector
import pickle
import os

# Load mô hình VGG16 (không bao gồm lớp fully connected)
try:
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D()
    ])
except Exception as e:
    print(f"Lỗi khi tải mô hình VGG16: {e}")
    exit(1)

def extract_feature(image_path):
    try:
        # Kiểm tra xem file có tồn tại không
        if not os.path.exists(image_path):
            print(f"File không tồn tại: {image_path}")
            return None
        # Đọc và tiền xử lý ảnh
        img = cv2.imread(image_path)
        if img is None:
            print(f"Không thể đọc ảnh: {image_path}")
            return None
        img = cv2.resize(img, (224, 224))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        # Trích xuất đặc trưng
        feature = model.predict(img)
        return feature.flatten()
    except Exception as e:
        print(f"Lỗi khi trích xuất đặc trưng từ ảnh {image_path}: {e}")
        return None

# Kết nối CSDL
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Thay bằng mật khẩu của bạn nếu có
        database="qlthucung1"
    )
    cursor = db.cursor()
except mysql.connector.Error as e:
    print(f"Lỗi khi kết nối CSDL: {e}")
    exit(1)

# Lấy tất cả ảnh từ bảng thu_cung_metadata
try:
    cursor.execute("SELECT id, image_path FROM thu_cung_metadata")
    rows = cursor.fetchall()

    for row in rows:
        id, image_path = row
        print(f"Đang xử lý ảnh: {image_path}")
        feature = extract_feature(image_path)
        if feature is not None:
            # Lưu đặc trưng vào CSDL
            feature_blob = pickle.dumps(feature)
            cursor.execute("UPDATE thu_cung_metadata SET feature_vector = %s WHERE id = %s", (feature_blob, id))
            db.commit()
            print(f"Đã lưu đặc trưng cho ảnh {image_path} (ID: {id})")
        else:
            print(f"Không thể trích xuất đặc trưng cho ảnh {image_path} (ID: {id})")
except mysql.connector.Error as e:
    print(f"Lỗi khi truy vấn hoặc cập nhật CSDL: {e}")
finally:
    cursor.close()
    db.close()