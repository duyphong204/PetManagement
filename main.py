import sys
import os
import customtkinter as ctk
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from views.login_view import show_login_content
from views.main_view import create_home_window
from views.doctor_view import open_doctor_dashboard
from views.user_view import open_user_dashboard
from views.register_view import show_register_content

from controllers.login_controller import LoginController
def main():
    # Thiết lập giao diện
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme("blue")

    # Tạo cửa sổ chính
    root = ctk.CTk()
    root.title("Đăng nhập hệ thống")
    root.geometry("925x500+300+200")
    root.resizable(False, False)
    
    # Khởi tạo controller
    login_controller = LoginController(root)

    # Callback để mở giao diện chính
    def open_home_callback():
        # Xóa toàn bộ nội dung hiện tại trong root
        for widget in root.winfo_children():
            widget.destroy()
        role = login_controller.role  # Lấy vai trò từ controller
        user_data = login_controller.user_data  # Lấy dữ liệu người dùng từ controller

        # Kiểm tra vai trò và mở giao diện tương ứng
        if role == "admin":
            create_home_window(root)  # Mở giao diện Admin
        elif role == "bac_si":
            open_doctor_dashboard(root)  # Mở giao diện Bác sĩ
        elif role == "khach_hang":
            open_user_dashboard(root, user_data["id"])  # Mở giao diện Người dùng
        else:
            print("Vai trò không hợp lệ!")
        # Tạo giao diện chính
       # create_home_window(root)

    # Hiển thị giao diện đăng nhập 
    show_login_content(root, open_home_callback)

    # Chạy ứng dụng
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:  
        print(f"Lỗi khi chạy chương trình: {e}")
        