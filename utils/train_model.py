import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Tắt oneDNN để tăng tốc trên CPU

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from datetime import datetime

# Hàm tìm tất cả file ảnh trong thư mục (hỗ trợ thư mục lồng sâu)
def find_image_files(directory):
    image_extensions = ('.jpg', '.jpeg', '.png')
    image_paths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(image_extensions):
                image_paths.append(os.path.join(root, file))
    return image_paths

# Hàm tải dữ liệu cho phân loại chó/mèo (chỉ để lấy nhãn, không huấn luyện)
def load_pet_data_paths():
    pet_image_paths = []
    pet_labels = []  # 0: chó, 1: mèo
    train_dir = "dataset/train"
    
    if not os.path.exists(train_dir):
        print(f"Thư mục {train_dir} không tồn tại.")
        exit(1)

    # Tải từ các thư mục dog_* và cat_*
    for species_dir in os.listdir(train_dir):
        species_path = os.path.join(train_dir, species_dir)
        if not os.path.isdir(species_path) or species_dir in ['dang_phuc', 'Duy_Phong', 'Huy_Hoang', 'Nguyen_Van_A']:
            continue
                
        image_paths = find_image_files(species_path)
        if not image_paths:
            print(f"Không tìm thấy ảnh trong {species_path}")
            continue
                
        species_label = 0 if species_dir.startswith("dog") else 1  # 0: chó, 1: mèo
        for img_path in image_paths:
            pet_image_paths.append(img_path)
            pet_labels.append(species_label)

    if not pet_image_paths:
        print("Không tìm thấy ảnh nào cho phân loại chó/mèo.")
        exit(1)
    
    return np.array(pet_image_paths), np.array(pet_labels)

# Hàm tải dữ liệu cho nhận diện chủ
def load_owner_data_paths(max_images_per_owner=1000):
    image_paths = []
    labels = []
    owners = []
    train_dir = "dataset/train"
    
    if not os.path.exists(train_dir):
        print(f"Thư mục {train_dir} không tồn tại.")
        exit(1)

    # Chỉ tải từ các thư mục chủ
    for owner_name in ['dang_phuc', 'Duy_Phong', 'Huy_Hoang', 'Nguyen_Van_A']:
        owner_path = os.path.join(train_dir, owner_name)
        if not os.path.isdir(owner_path):
            continue
        
        if owner_name not in owners:
            owners.append(owner_name)
        count = 0
        owner_images = find_image_files(owner_path)
        for img_path in owner_images:
            if count >= max_images_per_owner:
                break
            image_paths.append(img_path)
            labels.append(owners.index(owner_name))
            count += 1
        
        print(f"Thư mục {owner_name} có {count} ảnh.")
        if count < 10:
            print(f"Cảnh báo: Thư mục {owner_name} chỉ có {count} ảnh. Nên có ít nhất 50 ảnh để mô hình học tốt hơn.")

    if not image_paths:
        print("Không tìm thấy ảnh nào cho nhận diện chủ.")
        exit(1)
    
    return np.array(image_paths), np.array(labels), owners

def train_owner_model_only():
    # Tải dữ liệu chó/mèo (chỉ để lấy nhãn, không huấn luyện)
    print("Đang tải dữ liệu cho phân loại chó/mèo (chỉ để lấy nhãn)...")
    pet_image_paths, pet_labels = load_pet_data_paths()
    print(f"Tổng số ảnh cho phân loại chó/mèo: {len(pet_image_paths)}")

    # Tải dữ liệu cho nhận diện chủ
    print("Đang tải dữ liệu cho nhận diện chủ...")
    owner_image_paths, owner_labels, owners = load_owner_data_paths()
    print(f"Tổng số ảnh cho nhận diện chủ: {len(owner_image_paths)}")

    # Chia dữ liệu thành train/val/test
    pet_train_paths, pet_test_paths, pet_train_labels, pet_test_labels = train_test_split(
        pet_image_paths, pet_labels, test_size=0.15, random_state=42
    )
    pet_train_paths, pet_val_paths, pet_train_labels, pet_val_labels = train_test_split(
        pet_train_paths, pet_train_labels, test_size=0.1765, random_state=42
    )

    owner_train_paths, owner_test_paths, owner_train_labels, owner_test_labels = train_test_split(
        owner_image_paths, owner_labels, test_size=0.15, random_state=42
    )
    owner_train_paths, owner_val_paths, owner_train_labels, owner_val_labels = train_test_split(
        owner_train_paths, owner_train_labels, test_size=0.1765, random_state=42
    )

    # Tạo ImageDataGenerator cho phân loại chó/mèo (chỉ để lấy nhãn)
    pet_datagen = ImageDataGenerator(rescale=1./255)
    batch_size = 128
    pet_train_generator = pet_datagen.flow_from_dataframe(
        dataframe=pd.DataFrame({"filename": pet_train_paths, "class": pet_train_labels.astype(str)}),
        x_col="filename",
        y_col="class",
        target_size=(160, 160),
        batch_size=batch_size,
        class_mode='binary',
        shuffle=True
    )

    # Tạo ImageDataGenerator cho nhận diện chủ
    val_datagen = ImageDataGenerator(rescale=1./255)
    owner_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,  # Giảm augmentation
        width_shift_range=0.2,
        height_shift_range=0.2,
        zoom_range=[0.8, 1.2],
        horizontal_flip=True,
        brightness_range=[0.8, 1.2]
    )

    owner_train_generator = owner_datagen.flow_from_dataframe(
        dataframe=pd.DataFrame({"filename": owner_train_paths, "class": owner_train_labels.astype(str)}),
        x_col="filename",
        y_col="class",
        target_size=(128, 128),
        batch_size=8,
        class_mode='categorical',
        shuffle=True
    )

    owner_val_generator = val_datagen.flow_from_dataframe(
        dataframe=pd.DataFrame({"filename": owner_val_paths, "class": owner_val_labels.astype(str)}),
        x_col="filename",
        y_col="class",
        target_size=(128, 128),
        batch_size=8,
        class_mode='categorical',
        shuffle=False
    )

    owner_test_generator = val_datagen.flow_from_dataframe(
        dataframe=pd.DataFrame({"filename": owner_test_paths, "class": owner_test_labels.astype(str)}),
        x_col="filename",
        y_col="class",
        target_size=(128, 128),
        batch_size=8,
        class_mode='categorical',
        shuffle=False
    )

    # Xây dựng và huấn luyện mô hình nhận diện chủ
    print("Đang xây dựng mô hình nhận diện chủ...")
    owner_base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(128, 128, 3), alpha=0.35)
    owner_base_model.trainable = False  # Tắt fine-tuning

    owner_model = Sequential([
        owner_base_model,
        GlobalAveragePooling2D(),
        Dense(32, activation='relu'),
        Dropout(0.4),
        Dense(len(owners), activation='softmax')
    ])

    owner_model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    print("Đang huấn luyện mô hình nhận diện chủ...")
    owner_model.fit(
        owner_train_generator,
        validation_data=owner_val_generator,
        epochs=15,  # Giảm số epoch
        callbacks=[early_stopping]
    )

    # Đánh giá mô hình trên tập test
    test_loss, test_acc = owner_model.evaluate(owner_test_generator)
    print(f"Độ chính xác trên tập kiểm tra (nhận diện chủ): {test_acc}")

    # Lưu mô hình nhận diện chủ
    os.makedirs("models", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    owner_model_filename = f"models/owner_recognition_model_{timestamp}.keras"
    owner_model.save(owner_model_filename)
    print(f"Đã lưu mô hình nhận diện chủ tại {owner_model_filename}")

    # Lưu danh sách chủ
    with open("models/owners_list.txt", "w") as f:
        for owner in owners:
            f.write(f"{owner}\n")

    # Kiểm tra nhãn chó/mèo và chủ sở hữu
    print("Nhãn chó/mèo:", pet_train_generator.class_indices)
    print("Nhãn chủ sở hữu:", owner_train_generator.class_indices)

if __name__ == "__main__":
    train_owner_model_only()