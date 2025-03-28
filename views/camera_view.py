# views/camera_view.py
import customtkinter as ctk
import cv2
from PIL import Image
from utils.pet_recognition import initialize_model_and_db, recognize_pet_from_image, get_webcam_frame

def show_camera_content(frame):
    # Xóa nội dung hiện tại của frame
    for widget in frame.winfo_children():
        widget.destroy()

    # Tạo frame chứa webcam và các nút
    webcam_frame = ctk.CTkFrame(frame, fg_color="white")
    webcam_frame.pack(pady=10)

    # Label để hiển thị video từ webcam
    video_label = ctk.CTkLabel(webcam_frame, text="")
    video_label.pack(pady=10)

    # Label để hiển thị kết quả
    result_label = ctk.CTkLabel(webcam_frame, text="", font=("Arial", 14), text_color="black")
    result_label.pack(pady=10)

    # Biến để kiểm soát webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        result_label.configure(text="Không thể mở webcam. Hãy kiểm tra webcam của bạn.")
        return

    # Biến để kiểm soát trạng thái webcam
    is_running = True

    def update_frame():
        if not is_running:
            return
        frame = get_webcam_frame(cap)
        if frame is not None:
            # Chuyển frame từ BGR (OpenCV) sang RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Resize frame để hiển thị trên giao diện
            frame = cv2.resize(frame, (320, 240))
            # Chuyển frame thành CTkImage để hiển thị trên CustomTkinter
            image = Image.fromarray(frame)
            ctk_image = ctk.CTkImage(light_image=image, size=(320, 240))
            # Cập nhật video label
            video_label.configure(image=ctk_image)
        # Lặp lại sau 10ms
        video_label.after(10, update_frame)

    def recognize_pet():
        frame = get_webcam_frame(cap)
        if frame is None:
            result_label.configure(text="Không thể chụp ảnh từ webcam!")
            return
        # Khởi tạo mô hình và kết nối CSDL
        if not initialize_model_and_db():
            result_label.configure(text="Lỗi khi tải mô hình hoặc kết nối CSDL!")
            return
        # Nhận diện thú cưng
        label, pet_name, owner_name, confidence, min_distance = recognize_pet_from_image(frame)
        if label:
            result_text = f"Đây là một {label} ({pet_name}). Chủ vật nuôi: {owner_name}\n"
            result_text += f"(Confidence: {confidence:.2f}, Distance: {min_distance:.4f})"
            result_label.configure(text=result_text)
        else:
            result_label.configure(text="Không thể nhận diện ảnh!")

    def stop_webcam():
        nonlocal is_running
        is_running = False
        cap.release()
        video_label.configure(image=None)  # Xóa video
        result_label.configure(text="Webcam đã được tắt.")

    # Nút nhận diện
    recognize_button = ctk.CTkButton(webcam_frame, text="Nhận diện", font=("Arial", 14), 
                                     corner_radius=10, width=200, height=40, 
                                     fg_color="#34495E", hover_color="#2C3E50",
                                     command=recognize_pet)
    recognize_button.pack(pady=10)

    # Nút tắt webcam
    stop_button = ctk.CTkButton(webcam_frame, text="Tắt Webcam", font=("Arial", 14), 
                                corner_radius=10, width=200, height=40, 
                                fg_color="#C0392B", hover_color="#922B21",
                                command=stop_webcam)
    stop_button.pack(pady=10)

    # Bắt đầu hiển thị video
    update_frame()