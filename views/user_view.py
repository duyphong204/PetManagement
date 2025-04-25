
import customtkinter as ctk
import sys
import os
import views.manage_pet as manage_pet
from views.manage_customer import open_manage_customer_content
from views.medicine_warehouse import open_manage_medicine_content
from controllers.user_controller import UserController
from utils.connect_dtb import connect_db
from views.user_appointment_view import open_user_appointment_content


sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def show_home_content(frame):
    label = ctk.CTkLabel(frame, text="Chào mừng đến với hệ thống!", 
                         font=("Arial", 18, "bold"), text_color="black")
    label.pack(pady=30)

def open_user_dashboard(root, user_id):
    # Xóa nội dung hiện tại của root
    for widget in root.winfo_children():
        widget.destroy()

    # Cấu hình lại cửa sổ
    root.title("Quản lý Phòng Khám Thú Y")
    root.geometry("1200x650")

    # Sidebar
    sidebar = ctk.CTkFrame(root, width=250, height=850, corner_radius=0)
    sidebar.pack(side="left", fill="y")
    
    title_label = ctk.CTkLabel(sidebar, text="🐾 MENU", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    # Hàm để thay đổi nội dung chính
    def set_content(content_func):
        for widget in main_content.winfo_children():
            widget.destroy()
        content_func(main_content)

    # hàm đăng xuất
    def logout():
    # Xóa nội dung hiện tại của root
        from views.login_view import show_login_content
        for widget in root.winfo_children():
            widget.destroy()
    # Gọi giao diện đăng nhập, truyền root và callback để quay lại giao diện chính
        show_login_content(root, open_user_dashboard)

    # Danh sách nút menu
    buttons = [
        ("🏠 Trang chủ", lambda: set_content(show_home_content)),
        ("📝 Thông tin cá nhân", lambda: set_content(lambda frame: show_user_info_content(frame, user_id))),
        ("📅 Đặt hẹn khám", lambda: set_content(lambda frame: open_user_appointment_content(frame, user_id, connect_db))),
        ("🚪 Đăng xuất", logout),
    ]

    for btn_text, command in buttons:
        button = ctk.CTkButton(sidebar, text=btn_text, font=("Arial", 14), 
                               corner_radius=10, width=220, height=40, 
                               fg_color="#34495E", hover_color="#2C3E50",
                               command=command if command else lambda: print(f"{btn_text} thành công"))
        button.pack(pady=8)

    # Nội dung chính
    main_content = ctk.CTkFrame(root, fg_color="white", width=950, height=850)
    main_content.pack(side="right", fill="both", expand=True)

  # Hiển thị thông tin người dùng
    def show_user_info_content(frame, user_id):
     
        user_controller = UserController()
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

  

    return root

def open_home():
    root = ctk.CTk()
    open_user_dashboard(root)
    root.mainloop()

if __name__ == "__main__":
    open_home()