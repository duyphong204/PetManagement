
import customtkinter as ctk
import sys
import os
import views.manage_pet as manage_pet
from views.manage_customer import open_manage_customer_content
from views.manage_customer import open_manage_customer_content
from views.medicine_warehouse import open_manage_medicine_content
from views.KeDon_view import open_manage_prescription_content
import views.manage_doctor_view as manage_doctor
import views.quanlythuoc_view as quanlythuoc
import views.report_view as report_view
from controllers.report_controller import ReportController



sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def show_home_content(frame):
    label = ctk.CTkLabel(frame, text="Chào mừng đến với hệ thống!", 
                         font=("Arial", 18, "bold"), text_color="black")
    label.pack(pady=30)

def open_doctor_dashboard(root):
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
        show_login_content(root, open_doctor_dashboard)

    def show_report():
        import views.report_view as report_view
        report_controller = ReportController(main_content)
        report_controller.show_report()

    # Danh sách nút menu
    buttons = [
        ("🏠 Trang chủ", lambda: set_content(show_home_content)),
        ("🐶 Quản lý Thú cưng", lambda: set_content(manage_pet.open_manage_pet_content)),
        ("👥 Quản lý Khách hàng", lambda: set_content(open_manage_customer_content)),
        (" Quản lý bác sĩ", lambda: set_content(manage_doctor.open_manage_doctor_content)),
        (" Quản lý thuốc", lambda: set_content(quanlythuoc.open_manage_drug_content)),
        ("📷 Kê Đơn", lambda: set_content(open_manage_prescription_content)),
        ("📅 Lịch hẹn khám", None),
        ("📊 Báo cáo", lambda: show_report()),
        ("⚙️ Cài đặt", None),
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

    show_home_content(main_content)

    return root

def open_home():
    root = ctk.CTk()
    open_doctor_dashboard(root)
    root.mainloop()

if __name__ == "__main__":
    open_home()