import customtkinter as ctk
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from views.manage_pet import open_manage_pet  # Import giao diện quản lý thú cưng

# Cấu hình CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def open_home():
    home_root = ctk.CTk()
    home_root.title("Quản lý Phòng Khám Thú Y")
    home_root.geometry("930x478")

    # Sidebar
    sidebar = ctk.CTkFrame(home_root, width=250, height=478, corner_radius=0)
    sidebar.pack(side="left", fill="y")
    
    title_label = ctk.CTkLabel(sidebar, text="🐾 MENU", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    # Danh sách nút menu
    buttons = [
        ("🏠 Trang chủ", None),
        ("🐶 Quản lý Thú cưng", open_manage_pet),  # Gọi hàm Quản lý Thú cưng
        ("📅 Lịch hẹn khám", None),
        ("📊 Báo cáo", None),
        ("⚙️ Cài đặt", None),
        ("📷 Camera", None),
    ]

    for btn_text, command in buttons:
        button = ctk.CTkButton(sidebar, text=btn_text, font=("Arial", 14), 
                               corner_radius=10, width=220, height=40, 
                               fg_color="#34495E", hover_color="#2C3E50",
                               command=command)
        button.pack(pady=8)

    # Nội dung chính
    main_content = ctk.CTkFrame(home_root, fg_color="white", width=680, height=478)
    main_content.pack(side="right", fill="both", expand=True)

    label = ctk.CTkLabel(main_content, text="Chào mừng đến với hệ thống!", 
                         font=("Arial", 18, "bold"), text_color="black")
    label.pack(pady=30)

    home_root.mainloop()

# Chạy chương trình
# if __name__ == "__main__":
#     open_home()
