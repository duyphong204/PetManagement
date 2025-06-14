import sys
import os
import customtkinter as ctk
# Tắt cảnh báo TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from views.login_view import show_login_content
from views.main_view import create_home_window
from views.register_view import show_register_content

def main():
    # Thiết lập giao diện
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("blue")

    # Tạo cửa sổ chính
    root = ctk.CTk()
    root.title("Đăng nhập hệ thống")
    root.geometry("925x500+300+200")
    root.resizable(False, False)

    # Callback để mở giao diện chính
    def open_home_callback(root):
        # Xóa toàn bộ nội dung hiện tại trong root
        for widget in root.winfo_children():
            widget.destroy()
        # Tạo giao diện chính
        create_home_window(root)

    # Xử lý đóng cửa sổ
    def on_closing():
        # Xóa tất cả widget trước khi hủy
        for widget in root.winfo_children():
            widget.destroy()
        # Hủy tất cả tác vụ after còn lại (thủ công)
        try:
            # Hủy các tác vụ after của Tkinter
            root.tk.call('after', 'cancel', 'all')
            # Đảm bảo không còn tác vụ nào được lên lịch
            root.update_idletasks()
        except:
            pass
        # Hủy cửa sổ chính
        try:
            root.destroy()
        except:
            pass

    # Hiển thị giao diện đăng nhập 
    show_login_content(root, open_home_callback)

    # Gán sự kiện đóng cửa sổ
    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Chạy ứng dụng
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:  
        print(f"Lỗi khi chạy chương trình: {e}")