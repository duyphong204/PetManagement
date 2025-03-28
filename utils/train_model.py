# utils/train_model.py
import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split

# Hàm tiền xử lý ảnh
def preprocess_image(image_path, label):
    # Đọc và giải mã ảnh
    img = tf.io.read_file(image_path)
    img = tf.image.decode_jpeg(img, channels=3)
    # Resize ảnh
    img = tf.image.resize(img, [224, 224])
    # Chuẩn hóa giá trị pixel về [0, 1]
    img = img / 255.0
    return img, label

# Tạo dataset từ danh sách đường dẫn ảnh
def create_dataset(image_paths, labels, batch_size=32):
    dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))
    dataset = dataset.map(preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.shuffle(buffer_size=1000)
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    return dataset

# Tải danh sách đường dẫn ảnh và nhãn
# utils/train_model.py
def load_data_paths(max_images_per_class=2500):  # Giới hạn 2,500 ảnh mỗi lớp (tổng cộng 5,000 ảnh)
    image_paths = []
    labels = []  # 0: cat, 1: dog
    train_dir = "dataset/train"
    if not os.path.exists(train_dir):
        print(f"Thư mục {train_dir} không tồn tại. Hãy chạy 'prepare_dataset.py' trước!")
        exit(1)

    dog_count = 0
    cat_count = 0
    for subdir in os.listdir(train_dir):
        subdir_path = os.path.join(train_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue
        if "dog" in subdir:
            for img_name in os.listdir(subdir_path):
                if dog_count >= max_images_per_class:
                    break
                img_path = os.path.join(subdir_path, img_name)
                image_paths.append(img_path)
                labels.append(1)  # Dog
                dog_count += 1
        elif "cat" in subdir:
            for img_name in os.listdir(subdir_path):
                if cat_count >= max_images_per_class:
                    break
                img_path = os.path.join(subdir_path, img_name)
                image_paths.append(img_path)
                labels.append(0)  # Cat
                cat_count += 1
    if not image_paths:
        print("Không tìm thấy ảnh nào trong dataset. Hãy kiểm tra thư mục 'dataset/train'.")
        exit(1)
    return image_paths, labels

# Tải danh sách đường dẫn và nhãn
print("Đang tải danh sách đường dẫn ảnh...")
image_paths, labels = load_data_paths()

# Chia dữ liệu thành tập huấn luyện, xác nhận và kiểm tra
image_paths_train, image_paths_temp, labels_train, labels_temp = train_test_split(
    image_paths, labels, test_size=0.2, random_state=42
)
image_paths_val, image_paths_test, labels_val, labels_test = train_test_split(
    image_paths_temp, labels_temp, test_size=0.5, random_state=42
)

# Tạo dataset cho huấn luyện, xác nhận và kiểm tra
batch_size = 32
train_dataset = create_dataset(image_paths_train, labels_train, batch_size)
val_dataset = create_dataset(image_paths_val, labels_val, batch_size)
test_dataset = create_dataset(image_paths_test, labels_test, batch_size)

# Xây dựng mô hình MobileNetV2
print("Đang xây dựng mô hình...")
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
predictions = Dense(1, activation='sigmoid')(x)
model = Model(inputs=base_model.input, outputs=predictions)

# Đóng băng các tầng của mô hình pre-trained
for layer in base_model.layers:
    layer.trainable = False

# Huấn luyện mô hình
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print("Đang huấn luyện mô hình...")
model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=5,
    steps_per_epoch=len(image_paths_train) // batch_size,
    validation_steps=len(image_paths_val) // batch_size
)

# Lưu mô hình
os.makedirs("models", exist_ok=True)
model.save("models/pet_recognition_model.keras")
print("Đã lưu mô hình tại models/pet_recognition_model.keras")

# Đánh giá mô hình
test_loss, test_acc = model.evaluate(test_dataset, steps=len(image_paths_test) // batch_size)
print(f"Độ chính xác trên tập kiểm tra: {test_acc}")