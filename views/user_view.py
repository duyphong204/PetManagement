import customtkinter as ctk
from models.login_model import LoginModel
from controllers.user_controller import UserController
from config import config
db_config = config.db_config

def open_user_dashboard(user_id):
    user_root = ctk.CTk()
    user_root.title("User Dashboard")
    user_root.geometry("1200x850")

    # Sidebar
    sidebar = ctk.CTkFrame(user_root, width=250, height=850, corner_radius=0)
    sidebar.pack(side="left", fill="y")

    title_label = ctk.CTkLabel(sidebar, text="🐾 MENU - Khách hàng", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    # Hàm để thay đổi nội dung chính
    def set_content(content_func):
        for widget in main_content.winfo_children():
            widget.destroy()
        content_func(main_content)

    # Danh sách các nút menu cho Khách hàng
    buttons = [
        ("🏠 Trang chủ", lambda: set_content(show_home_content)),
        ("📝 Thông tin cá nhân", lambda: set_content(lambda frame: show_user_info_content(frame, user_id))),
        ("📅 Lịch hẹn khám", lambda: set_content(lambda frame: show_appointment_content(frame, user_id))),
        ("💊 Đơn thuốc", None),
    ]

    for btn_text, command in buttons:
        button = ctk.CTkButton(sidebar, text=btn_text, font=("Arial", 14), 
                               corner_radius=10, width=220, height=40, 
                               fg_color="#34495E", hover_color="#2C3E50",
                               command=command if command else None)
        button.pack(pady=8)

    # Nút đăng xuất
    logout_button = ctk.CTkButton(sidebar, text="🚪 Đăng xuất", font=("Arial", 14), 
                                  corner_radius=10, width=220, height=40, fg_color="red", 
                                  hover_color="#8B0000", command=user_root.destroy)
    logout_button.pack(pady=20)

    # Nội dung chính (ban đầu)
    main_content = ctk.CTkFrame(user_root, fg_color="white", width=950, height=850)
    main_content.pack(side="right", fill="both", expand=True)

    def show_home_content(frame):
        label = ctk.CTkLabel(frame, text="Chào mừng đến với hệ thống của Khách hàng!", 
                             font=("Arial", 18, "bold"), text_color="black")
        label.pack(pady=30)

    def show_user_info_content(frame, user_id):
        """Hiển thị thông tin người dùng"""
        user_controller = UserController(db_config)
        user_info = user_controller.get_user_info(user_id)

        if user_info:
            user_frame = ctk.CTkFrame(frame, fg_color="#f0f0f0", corner_radius=10, width=900, height=500)
            user_frame.pack(pady=20, padx=20, fill="both", expand=True)

            # Tiêu đề
            title = ctk.CTkLabel(user_frame, text="Thông Tin Cá Nhân", font=("Arial", 20, "bold"), text_color="white", fg_color="#2C3E50", width=900)
            title.pack(pady=20)

            # Tạo frame chứa bảng thông tin cá nhân
            table_frame = ctk.CTkFrame(user_frame, corner_radius=10, width=800, border_width=2, border_color="#cccccc")
            table_frame.pack(pady=10, padx=20, fill="both", expand=True)

            # Tiêu đề các cột
            headers = ['ID', 'Tên', 'Số điện thoại', 'Email', 'Địa chỉ']
            for i, header in enumerate(headers):
                header_label = ctk.CTkLabel(table_frame, text=header, font=("Arial", 14, "bold"), width=150, anchor="w", padx=10)
                header_label.grid(row=0, column=i, padx=10, pady=10, sticky="w")

            # Dữ liệu người dùng
            user_data = [
                user_info['id'], 
                user_info['ho_ten'], 
                user_info['so_dien_thoai'], 
                user_info['email'], 
                user_info['dia_chi'], 
            ]

            # Hiển thị dữ liệu người dùng vào bảng
            for i, data in enumerate(user_data):
                data_label = ctk.CTkLabel(table_frame, text=data, font=("Arial", 14), width=150, anchor="w", padx=10)
                data_label.grid(row=1, column=i, padx=10, pady=10, sticky="w")

        else:
            error_label = ctk.CTkLabel(frame, text="Không tìm thấy thông tin cá nhân!", 
                                       font=("Arial", 18, "bold"), text_color="red")
            error_label.pack(pady=30)

    def show_appointment_content(frame, user_id):
        """Hiển thị các lịch hẹn"""
        user_controller = UserController(db_config)
        appointments = user_controller.get_appointments_info(user_id)

        if appointments:
            appointment_frame = ctk.CTkFrame(frame, fg_color="#f0f0f0", corner_radius=10, width=900, height=500)
            appointment_frame.pack(pady=20, padx=20, fill="both", expand=True)

            title = ctk.CTkLabel(appointment_frame, text="Lịch Hẹn Khám", font=("Arial", 20, "bold"), text_color="white", fg_color="#2C3E50", width=900)
            title.pack(pady=20)

            # Tạo frame chứa bảng lịch hẹn
            table_frame = ctk.CTkFrame(appointment_frame, corner_radius=10, width=800, border_width=2, border_color="#cccccc")
            table_frame.pack(pady=10, padx=20, fill="both", expand=True)

            # Tiêu đề cột
            headers = ['ID', 'Ngày hẹn', 'Giờ hẹn', 'ID thú cưng', 'ID bác sĩ', 'Trạng thái']
            for i, header in enumerate(headers):
                header_label = ctk.CTkLabel(table_frame, text=header, font=("Arial", 14, "bold"), width=150, anchor="w", padx=10)
                header_label.grid(row=0, column=i, padx=10, pady=10, sticky="w")

            # Lặp qua tất cả các lịch hẹn trong appointments
            for row, appointment in enumerate(appointments, start=1):
                # Dữ liệu cho mỗi lịch hẹn
                appointment_data = [
                    appointment['id'], 
                    appointment['ngay_hen'], 
                    appointment['gio_hen'],
                    appointment['id_thu_cung'],
                    appointment['id_bac_si'], 
                    appointment['trang_thai'],     
                ]

                # Hiển thị dữ liệu lịch hẹn vào bảng
                for col, data in enumerate(appointment_data):
                    data_label = ctk.CTkLabel(table_frame, text=data, font=("Arial", 14), width=150, anchor="w", padx=10)
                    data_label.grid(row=row, column=col, padx=10, pady=10, sticky="w")

        else:
            error_label = ctk.CTkLabel(frame, text="Không tìm thấy lịch hẹn !", 
                                       font=("Arial", 18, "bold"), text_color="red")
            error_label.pack(pady=30)

    # Show the home page initially
    show_home_content(main_content)

    user_root.mainloop()