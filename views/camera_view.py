import customtkinter as ctk
import cv2
from PIL import Image
from utils.pet_recognition import initialize_model_and_db, recognize_pet_from_image, get_webcam_frame

def show_camera_content(frame):
    # Xóa nội dung cũ
    for widget in frame.winfo_children():
        widget.destroy()

    # Tạo giao diện
    webcam_frame = ctk.CTkFrame(frame, fg_color="white")
    webcam_frame.pack(pady=10)
    video_label = ctk.CTkLabel(webcam_frame, text="")
    video_label.pack(pady=10)
    result_label = ctk.CTkLabel(webcam_frame, text="", font=("Arial", 14), text_color="black")
    result_label.pack(pady=10)

    # Khởi động webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        result_label.configure(text="Không thể mở webcam!")
        return

    is_running = True

    def update_frame():
        if not is_running:
            return
        frame = get_webcam_frame(cap)
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (320, 240))
            ctk_image = ctk.CTkImage(light_image=Image.fromarray(frame), size=(320, 240))
            video_label.configure(image=ctk_image)
        video_label.after(10, update_frame)

    def recognize_pet():
        frame = get_webcam_frame(cap)
        if frame is None or not initialize_model_and_db():
            result_label.configure(text="Lỗi chụp ảnh hoặc khởi tạo!")
            return
        label, pet_name, owner_name, confidence, min_distance, appointment_info = recognize_pet_from_image(frame)
        result_text = f"{label} ({pet_name}). Chủ: {owner_name}\n(Confidence: {confidence:.2f}, Distance: {min_distance:.4f})\n{appointment_info}"
        result_label.configure(text=result_text)

    def stop_webcam():
        nonlocal is_running
        is_running = False
        cap.release()
        video_label.configure(image=None)
        result_label.configure(text="Webcam đã tắt.")

    # Tạo nút
    ctk.CTkButton(webcam_frame, text="Nhận diện", font=("Arial", 14), corner_radius=10, width=200, height=40,
                  fg_color="#34495E", hover_color="#2C3E50", command=recognize_pet).pack(pady=10)
    ctk.CTkButton(webcam_frame, text="Tắt Webcam", font=("Arial", 14), corner_radius=10, width=200, height=40,
                  fg_color="#C0392B", hover_color="#922B21", command=stop_webcam).pack(pady=10)

    update_frame()