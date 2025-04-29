import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import customtkinter as ctk
import cv2
from PIL import Image
from utils.pet_recognition import PetRecognizer

def show_camera_content(frame):
    recognizer = PetRecognizer()

    for widget in frame.winfo_children():
        widget.destroy()

    webcam_frame = ctk.CTkFrame(frame, fg_color="white")
    webcam_frame.pack(pady=10)
    video_label = ctk.CTkLabel(webcam_frame, text="")
    video_label.pack(pady=10)
    result_label = ctk.CTkLabel(webcam_frame, text="", font=("Arial", 14), text_color="black", justify="left", anchor="w")
    result_label.pack(pady=10, fill="x", padx=10)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        result_label.configure(text="Không thể mở webcam!")
        return

    if not recognizer.initialize():
        result_label.configure(text="Lỗi khởi tạo mô hình hoặc cơ sở dữ liệu! Vui lòng kiểm tra lại.")
        if cap:
            cap.release()
        return

    video_label.is_running = True
    video_label.after_id = None
    video_label.last_frame = None

    def update_frame():
        if not getattr(video_label, 'is_running', False):
            return
        frame = recognizer.get_webcam_frame(cap)
        if frame is not None:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_resized = cv2.resize(frame_rgb, (320, 240))
            video_label.last_frame = frame
            ctk_image = ctk.CTkImage(light_image=Image.fromarray(frame_resized), size=(320, 240))
            video_label.configure(image=ctk_image)
        video_label.after_id = video_label.after(10, update_frame)

    def recognize_pet():
        frame = getattr(video_label, 'last_frame', None)
        if frame is None:
            frame = recognizer.get_webcam_frame(cap)
            if frame is None:
                result_label.configure(text="Lỗi chụp ảnh! Vui lòng kiểm tra webcam.")
                return
        
        try:
            result = recognizer.recognize_pet_and_owner(frame=frame)
            
            # Chỉ hiển thị loài nếu không có thông tin chủ
            species_text = f"Loài: {result['species']} (Confidence: {result['species_confidence']:.2f})"
            if result['owner_info']['ho_ten'] == "Không xác định":
                result_text = f"{species_text}\nKhông xác định được chủ sở hữu."
            else:
                owner_text = f"Chủ: {result['owner_info']['ho_ten']} (Confidence: {result['owner_confidence']:.2f})"
                owner_details = f"SĐT: {result['owner_info']['so_dien_thoai']}\nĐịa chỉ: {result['owner_info']['dia_chi']}"
                pet_text = "Thú cưng: "
                if result['pets']:
                    pet_text += "\n" + "\n".join([f"- {pet['ten']} ({pet['loai']}, {pet['tuoi']} tuổi, {pet['gioi_tinh']})" for pet in result['pets']])
                else:
                    pet_text += "Không tìm thấy"
                if result['pet_appointment']:
                    appointment_time = f"{result['pet_appointment']['ngay_hen']} {result['pet_appointment']['gio_hen']}"
                    appointment_text = f"Lịch hẹn: {result['pet_appointment']['ten']} - {appointment_time} ({result['pet_appointment']['trang_thai']})"
                else:
                    appointment_text = "Không có lịch hẹn"
                result_text = f"{species_text}\n{owner_text}\n{owner_details}\n{pet_text}\n{appointment_text}"
            
            result_label.configure(text=result_text)
        except Exception as e:
            result_label.configure(text=f"Lỗi nhận diện: {str(e)}")

    def stop_webcam():
        video_label.is_running = False
        if getattr(video_label, 'after_id', None):
            try:
                video_label.after_cancel(video_label.after_id)
                video_label.after_id = None
            except:
                pass
        if cap:
            cap.release()
        try:
            video_label.configure(image=None)
            result_label.configure(text="Webcam đã tắt.")
        except:
            pass
        recognizer.close()

    ctk.CTkButton(webcam_frame, text="Nhận diện", font=("Arial", 14), corner_radius=10, width=200, height=40,
                  fg_color="#34495E", hover_color="#2C3E50", command=recognize_pet).pack(pady=10)
    ctk.CTkButton(webcam_frame, text="Tắt Webcam", font=("Arial", 14), corner_radius=10, width=200, height=40,
                  fg_color="#C0392B", hover_color="#922B21", command=stop_webcam).pack(pady=10)

    video_label.bind("<Destroy>", lambda _: stop_webcam())
    update_frame()