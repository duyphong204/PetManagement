import sys
import os
import customtkinter as ctk
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from views.login_view import show_login_content
from views.main_view import create_home_window

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Tạo cửa sổ chính duy nhất
    root = ctk.CTk()
    root.title("Đăng nhập hệ thống")
    root.geometry("925x500+300+200")
    root.resizable(False, False)

    def open_home_callback(root):
        create_home_window(root)

    # Hiển thị giao diện đăng nhập
    show_login_content(root, open_home_callback)

    # Chạy mainloop cho cửa sổ chính
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Lỗi khi chạy chương trình: {e}")