import customtkinter as ctk
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from views.manage_pet import open_manage_pet_content

# Cấu hình CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def open_home():
    home_root = ctk.CTk()
    home_root.title("Quản lý Phòng Khám Thú Y")
    home_root.geometry("1200x850")  # Tăng chiều cao để hiển thị nút dưới bảng

    # Sidebar
    sidebar = ctk.CTkFrame(home_root, width=250, height=850, corner_radius=0)
    sidebar.pack(side="left", fill="y")
    
    title_label = ctk.CTkLabel(sidebar, text="🐾 MENU", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    # Hàm để thay đổi nội dung chính
    def set_content(content_func):
        for widget in main_content.winfo_children():
            widget.destroy()
        content_func(main_content)

    # Danh sách nút menu
    buttons = [
        ("🏠 Trang chủ", lambda: set_content(show_home_content)),
        ("🐶 Quản lý Thú cưng", lambda: set_content(open_manage_pet_content)),
        ("📅 Lịch hẹn khám", None),
        ("📊 Báo cáo", None),
        ("⚙️ Cài đặt", None),
        ("📷 Camera", None),
    ]

    for btn_text, command in buttons:
        button = ctk.CTkButton(sidebar, text=btn_text, font=("Arial", 14), 
                               corner_radius=10, width=220, height=40, 
                               fg_color="#34495E", hover_color="#2C3E50",
                               command=command if command else None)
        button.pack(pady=8)

    # Nội dung chính (ban đầu)
    main_content = ctk.CTkFrame(home_root, fg_color="white", width=950, height=850)
    main_content.pack(side="right", fill="both", expand=True)

    def show_home_content(frame):
        label = ctk.CTkLabel(frame, text="Chào mừng đến với hệ thống!", 
                             font=("Arial", 18, "bold"), text_color="black")
        label.pack(pady=30)

    show_home_content(main_content)

    home_root.mainloop()

if __name__ == "__main__":
    open_home()