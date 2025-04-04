import customtkinter as ctk
from views.manage_pet import open_manage_pet_content
from views.manage_customer import open_manage_customer_content

# Cấu hình CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def open_doctor_dashboard():
    """Hiển thị giao diện Doctor Dashboard"""
    # Tạo cửa sổ mới cho Doctor Dashboard
    doctor_root = ctk.CTk()
    doctor_root.title("Doctor Dashboard")
    doctor_root.geometry("1200x850")  # Tăng chiều cao để hiển thị các nút dưới bảng

    # Sidebar
    sidebar = ctk.CTkFrame(doctor_root, width=250, height=850, corner_radius=0)
    sidebar.pack(side="left", fill="y")
    
    title_label = ctk.CTkLabel(sidebar, text="🐾 MENU - Bác sĩ", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    # Hàm để thay đổi nội dung chính
    def set_content(content_func):
        for widget in main_content.winfo_children():
            widget.destroy()
        content_func(main_content)

    # Danh sách các nút menu cho Bác sĩ
    buttons = [
        ("🏠 Trang chủ", lambda: set_content(show_home_content)),
        ("🐶 Quản lý Thú cưng", lambda: set_content(open_manage_pet_content)),
        ("👥 Quản lý Khách hàng", lambda: set_content(open_manage_customer_content)),
        ("📅 Lịch hẹn khám", None),  # Có thể thêm chức năng quản lý lịch hẹn khám
        ("💊 Kê đơn thuốc", None),   # Có thể thêm chức năng kê đơn thuốc
    ]

    # Thêm các nút vào sidebar
    for btn_text, command in buttons:
        button = ctk.CTkButton(sidebar, text=btn_text, font=("Arial", 14), 
                               corner_radius=10, width=220, height=40, 
                               fg_color="#34495E", hover_color="#2C3E50",
                               command=command if command else None)
        button.pack(pady=8)

    # Nút Đăng xuất
    logout_button = ctk.CTkButton(sidebar, text="🚪 Đăng xuất", font=("Arial", 14), 
                                  corner_radius=10, width=220, height=40, fg_color="red", 
                                  hover_color="#8B0000", command=doctor_root.destroy)
    logout_button.pack(pady=20)

    # Nội dung chính (ban đầu)
    main_content = ctk.CTkFrame(doctor_root, fg_color="white", width=950, height=850)
    main_content.pack(side="right", fill="both", expand=True)

    def show_home_content(frame):
        label = ctk.CTkLabel(frame, text="Chào mừng đến với hệ thống quản lý Bác sĩ!", 
                             font=("Arial", 18, "bold"), text_color="black")
        label.pack(pady=30)

    show_home_content(main_content)

    doctor_root.mainloop()

if __name__ == "__main__":
    open_doctor_dashboard()
