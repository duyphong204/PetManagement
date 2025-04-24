import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import pandas as pd
import os
import shutil

# Lấy thư mục gốc của dự án (dù chạy từ thư mục utils/)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
TRAIN_DIR = os.path.join(DATASET_DIR, "train")
VAL_DIR = os.path.join(DATASET_DIR, "val")

# Đổi tên thư mục test thành val (nếu cần)
if os.path.exists(os.path.join(DATASET_DIR, "test")):
    os.rename(os.path.join(DATASET_DIR, "test"), VAL_DIR)
    print("Đã đổi tên thư mục test thành val.")

# Kiểm tra thư mục dataset
if not os.path.exists(TRAIN_DIR) or not os.path.exists(VAL_DIR):
    raise FileNotFoundError("Thư mục train hoặc val không tồn tại. Vui lòng kiểm tra dataset.")

# Hàm lấy danh sách ảnh từ các thư mục cat_* và dog_* trực tiếp trong train/
def get_image_paths_and_labels(base_dir, prefix):
    image_paths = []
    labels = []
    if not os.path.exists(base_dir):
        print(f"Thư mục {base_dir} không tồn tại.")
        return image_paths, labels

    # Lấy danh sách các thư mục con
    subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    # Lọc các thư mục có tên bắt đầu bằng prefix (cat_ hoặc dog_)
    valid_subdirs = [d for d in subdirs if d.startswith(prefix)]
    
    if not valid_subdirs:
        print(f"Không tìm thấy thư mục nào bắt đầu bằng {prefix} trong {base_dir}.")
        return image_paths, labels

    for subdir in valid_subdirs:
        subdir_path = os.path.join(base_dir, subdir)
        files = os.listdir(subdir_path)
        image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if not image_files:
            print(f"Thư mục {subdir_path} không chứa ảnh (.jpg, .jpeg, .png).")
            continue
        for filename in image_files:
            image_path = os.path.join(subdir_path, filename)
            image_paths.append(image_path)
            labels.append(1 if prefix == "cat_" else 0)  # 1: cat, 0: dog
    
    return image_paths, labels

# Tạo danh sách ảnh và nhãn cho tập train
train_cat_paths, train_cat_labels = get_image_paths_and_labels(TRAIN_DIR, "cat_")
train_dog_paths, train_dog_labels = get_image_paths_and_labels(TRAIN_DIR, "dog_")

# Kết hợp danh sách ảnh và nhãn
train_image_paths = train_cat_paths + train_dog_paths
train_labels = train_cat_labels + train_dog_labels

# Kiểm tra nếu không tìm thấy ảnh
if not train_image_paths:
    raise ValueError("Không tìm thấy ảnh nào trong các thư mục cat_* hoặc dog_* trong tập train.")

# Tạo DataFrame cho tập train
train_df = pd.DataFrame({
    "filename": train_image_paths,
    "class": train_labels
})
train_df["class"] = train_df["class"].map({0: "dog", 1: "cat"})

# Tạo generator cho tập validation
val_datagen = ImageDataGenerator(rescale=1./255)
val_generator = val_datagen.flow_from_directory(
    VAL_DIR,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

# In thông tin
print(f"Số lượng ảnh trong tập train: {len(train_image_paths)}")
print(f"Số lượng ảnh mèo (train): {len(train_cat_paths)}")
print(f"Số lượng ảnh chó (train): {len(train_dog_paths)}")
print(f"Số lượng ảnh trong tập validation: {val_generator.samples}")
print(f"Nhãn lớp: {val_generator.class_indices}")

# Thiết lập tham số
IMG_SIZE = (224, 224)

BATCH_SIZE = 32
EPOCHS = 10

# Tạo ImageDataGenerator để tăng cường dữ liệu
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Tạo generator cho tập train từ DataFrame
train_generator = train_datagen.flow_from_dataframe(
    train_df,
    x_col="filename",
    y_col="class",
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

# Tải mô hình MobileNetV2
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Đóng băng các tầng của mô hình cơ sở
for layer in base_model.layers:
    layer.trainable = False

# Thêm các tầng tùy chỉnh
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(128, activation='relu')(x)
predictions = Dense(1, activation='sigmoid')(x)

# Tạo mô hình hoàn chỉnh
model = Model(inputs=base_model.input, outputs=predictions)

# Biên dịch mô hình
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Huấn luyện mô hình
history = model.fit(
    train_generator,
    epochs=EPOCHS,
    validation_data=val_generator
)

# Lưu mô hình thành file .keras
model.save(os.path.join(BASE_DIR, "models", "pet_recognition.keras"))
print("Đã lưu mô hình mới tại:", os.path.join(BASE_DIR, "models", "pet_recognition.keras"))

# In độ chính xác cuối cùng
final_train_accuracy = history.history['accuracy'][-1]
final_val_accuracy = history.history['val_accuracy'][-1]
print(f"Độ chính xác trên tập train: {final_train_accuracy:.2f}")
print(f"Độ chính xác trên tập validation: {final_val_accuracy:.2f}")