import numpy as np
import tensorflow as tf
import cv2
import os
from utils.connect_dtb import connect_db

class PetRecognizer:
    def __init__(self):
        # Đường dẫn đến các file mô hình
        self.PET_MODEL_PATH = "models/pet_recognition.keras"
        self.OWNER_MODEL_PATH = "models/owner_recognition_model_20250424_103623.keras"
        self.OWNERS_LIST_PATH = "models/owners_list.txt"

        # Ánh xạ tên thư mục với ho_ten trong bảng chu_so_huu
        self.OWNER_NAME_MAPPING = {
            "Nguyen_Van_A": "Nguyễn Văn Tiến",
            "dang_phuc": "Đăng phúc",
            "Duy_Phong": "Duy Phong",
            "Huy_Hoang": "Nguyễn Huy Hoàng",
        }

        # Giới hạn số luồng CPU
        tf.config.threading.set_intra_op_parallelism_threads(2)
        tf.config.threading.set_inter_op_parallelism_threads(2)

        self.pet_model = None
        self.owner_model = None
        self.owners_list = None
        self.db_connection = None

    def initialize(self):
        try:
            self.owners_list = self._load_owners_list()
            self.pet_model, self.owner_model = self._load_models()
            self.db_connection = connect_db()
            if self.db_connection and self.db_connection.is_connected():
                return True
            else:
                print("Không thể kết nối đến cơ sở dữ liệu!")
                return False
        except Exception as e:
            print(f"Lỗi khởi tạo mô hình hoặc cơ sở dữ liệu: {e}")
            return False

    def close(self):
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()
            self.db_connection = None

    def __del__(self):
        # Giải phóng mô hình khi đối tượng bị hủy
        self.pet_model = None
        self.owner_model = None
        self.close()

    def _load_owners_list(self):
        if not os.path.exists(self.OWNERS_LIST_PATH):
            raise FileNotFoundError(f"Không tìm thấy file {self.OWNERS_LIST_PATH}")
        with open(self.OWNERS_LIST_PATH, "r") as f:
            owners = [line.strip() for line in f.readlines()]
        return owners

    def _load_models(self):
        try:
            pet_model = tf.keras.models.load_model(self.PET_MODEL_PATH)
        except Exception as e:
            raise FileNotFoundError(f"Không thể tải pet_model từ {self.PET_MODEL_PATH}: {e}")
        try:
            owner_model = tf.keras.models.load_model(self.OWNER_MODEL_PATH)
        except Exception as e:
            raise FileNotFoundError(f"Không thể tải owner_model từ {self.OWNER_MODEL_PATH}: {e}")
        return pet_model, owner_model

    def adjust_brightness_if_needed(self, image):
        # Chuyển ảnh sang grayscale để tính độ sáng trung bình
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        brightness = np.mean(gray)
        print(f"Độ sáng trung bình của ảnh: {brightness:.2f}")
        
        # Nếu ảnh quá tối (độ sáng trung bình < 50), tăng độ sáng
        if brightness < 50:
            alpha = 1.0
            beta = 50  # Tăng độ sáng
            image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
            print("Ảnh quá tối, đã tăng độ sáng.")
        # Nếu ảnh quá sáng (độ sáng trung bình > 200), giảm độ sáng
        elif brightness > 200:
            alpha = 1.0
            beta = -50  # Giảm độ sáng
            image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
            print("Ảnh quá sáng, đã giảm độ sáng.")
        
        return image

    def preprocess_image_for_pet(self, image):
        # Kiểm tra và điều chỉnh độ sáng nếu cần, đồng thời áp dụng độ tương phản
        image = self.adjust_brightness_if_needed(image)
        
        # Chuyển sang RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Điều chỉnh độ sáng và độ tương phản (gộp vào một bước)
        alpha = 1.2  # Độ tương phản
        beta = 20    # Độ sáng
        image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        
        # Đảm bảo giá trị pixel trong khoảng [0, 255]
        image = np.clip(image, 0, 255)
        
        # Resize về kích thước phù hợp
        image = cv2.resize(image, (224, 224))
        image = image / 255.0
        image = np.expand_dims(image, axis=0)
        return image

    def preprocess_image_for_owner(self, image):
        # Kiểm tra và điều chỉnh độ sáng nếu cần, đồng thời chuyển sang RGB
        image = self.adjust_brightness_if_needed(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize về kích thước phù hợp
        image = cv2.resize(image, (128, 128))
        image = image / 255.0
        image = np.expand_dims(image, axis=0)
        return image

    def get_owner_and_pet_info(self, owner_dir_name, species):
        owner_name = self.OWNER_NAME_MAPPING.get(owner_dir_name, "Không xác định")
        if owner_name == "Không xác định":
            return None, [], None

        if not self.db_connection or not self.db_connection.is_connected():
            return None, [], None

        try:
            cursor = self.db_connection.cursor(dictionary=True)
            
            # Truy vấn thông tin chủ
            query_owner = """
            SELECT id, ho_ten, so_dien_thoai, dia_chi
            FROM chu_so_huu
            WHERE ho_ten = %s
            """
            cursor.execute(query_owner, (owner_name,))
            owner_info = cursor.fetchone()

            if not owner_info:
                cursor.close()
                return None, [], None

            # Truy vấn danh sách thú cưng
            query_pets = """
            SELECT id, ten, loai, tuoi, gioi_tinh
            FROM thu_cung
            WHERE id_chu_so_huu = %s AND loai LIKE %s
            """
            species_pattern = f"%{species}%"
            cursor.execute(query_pets, (owner_info['id'], species_pattern))
            pets = cursor.fetchall()

            # Truy vấn lịch hẹn
            pet_appointment = None
            if pets:
                pet_ids = [pet['id'] for pet in pets]
                if pet_ids:
                    if len(pet_ids) == 1:
                        query_appointment = """
                        SELECT lh.ngay_hen, lh.gio_hen, lh.trang_thai, tc.ten
                        FROM lich_hen lh
                        JOIN thu_cung tc ON lh.id_thu_cung = tc.id
                        WHERE lh.id_thu_cung = %s
                        ORDER BY lh.ngay_hen DESC, lh.gio_hen DESC
                        LIMIT 1
                        """
                        cursor.execute(query_appointment, (pet_ids[0],))
                    else:
                        query_appointment = """
                        SELECT lh.ngay_hen, lh.gio_hen, lh.trang_thai, tc.ten
                        FROM lich_hen lh
                        JOIN thu_cung tc ON lh.id_thu_cung = tc.id
                        WHERE lh.id_thu_cung IN (%s)
                        ORDER BY lh.ngay_hen DESC, lh.gio_hen DESC
                        LIMIT 1
                        """
                        placeholders = ','.join(['%s'] * len(pet_ids))
                        query_appointment = query_appointment % placeholders
                        cursor.execute(query_appointment, pet_ids)
                    pet_appointment = cursor.fetchone()

            cursor.close()
            return owner_info, pets, pet_appointment

        except Exception as e:
            print(f"Lỗi truy vấn CSDL: {e}")
            return None, [], None

    def recognize_pet_and_owner(self, image_path=None, frame=None):
        if self.pet_model is None or self.owner_model is None or self.owners_list is None:
            if not self.initialize():
                raise RuntimeError("Không thể khởi tạo mô hình hoặc danh sách chủ")

        if image_path:
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"Không thể đọc ảnh từ {image_path}")
        elif frame is not None:
            image = frame
        else:
            raise ValueError("Cần cung cấp image_path hoặc frame")

        pet_image = self.preprocess_image_for_pet(image)
        owner_image = self.preprocess_image_for_owner(image)

        # Dự đoán loài thú cưng
        pet_prediction = self.pet_model.predict(pet_image)
        pet_confidence = pet_prediction[0][0]  # Lấy giá trị sigmoid (0-1)
        print(f"Pet prediction confidence: {pet_confidence:.2f}")
        pet_label = "Mèo" if pet_confidence < 0.5 else "Chó"  # cat: 0, dog: 1

        owner_prediction = self.owner_model.predict(owner_image)
        owner_class = np.argmax(owner_prediction, axis=1)[0]
        owner_confidence = np.max(owner_prediction)
        print(f"Owner prediction confidence: {owner_confidence:.2f}")
        owner_name = self.owners_list[owner_class] if owner_class < len(self.owners_list) else "Không xác định"

        owner_info, pets, pet_appointment = self.get_owner_and_pet_info(owner_name, pet_label)

        result = {
            "species": pet_label,
            "species_confidence": float(pet_confidence),
            "owner_dir_name": owner_name,
            "owner_confidence": float(owner_confidence),
            "owner_info": owner_info if owner_info else {"ho_ten": "Không tìm thấy", "so_dien_thoai": "", "dia_chi": ""},
            "pets": pets if pets else [],
            "pet_appointment": pet_appointment if pet_appointment else None
        }

        return result

    @staticmethod
    def get_webcam_frame(cap):
        ret, frame = cap.read()
        if not ret:
            return None
        return frame

    @staticmethod
    def format_result_for_display(result):
        species_text = f"Loài: {result['species']} (Confidence: {result['species_confidence']:.2f})"
        owner_text = f"Chủ: {result['owner_info']['ho_ten']} (Confidence: {result['owner_confidence']:.2f})"
        owner_details = f"SĐT: {result['owner_info']['so_dien_thoai']}, Địa chỉ: {result['owner_info']['dia_chi']}"
        pet_text = "Thú cưng: "
        if result['pets']:
            pet_text += ", ".join([f"{pet['ten']} ({pet['loai']}, {pet['tuoi']} tuổi, {pet['gioi_tinh']})" for pet in result['pets']])
        else:
            pet_text += "Không tìm thấy"
        if result['pet_appointment']:
            appointment_time = f"{result['pet_appointment']['ngay_hen']} {result['pet_appointment']['gio_hen']}"
            appointment_text = f"Lịch hẹn: {result['pet_appointment']['ten']} - {appointment_time} ({result['pet_appointment']['trang_thai']})"
        else:
            appointment_text = "Không có lịch hẹn"
        return species_text, owner_text, owner_details, pet_text, appointment_text

    def recognize_from_webcam(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise ValueError("Không thể mở webcam")

        try:
            while True:
                frame = self.get_webcam_frame(cap)
                if frame is None:
                    print("Không thể đọc frame từ webcam")
                    break

                result = self.recognize_pet_and_owner(frame=frame)
                species_text, owner_text, owner_details, pet_text, appointment_text = self.format_result_for_display(result)

                cv2.putText(frame, species_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, owner_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, owner_details, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, pet_text, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, appointment_text, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                cv2.imshow("Pet Recognition", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.close()

if __name__ == "__main__":
    recognizer = PetRecognizer()
    recognizer.recognize_from_webcam()