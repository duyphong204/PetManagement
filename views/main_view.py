import customtkinter as ctk
import sys
import os
from PIL import Image
# Tắt oneDNN để tránh cảnh báo
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import views.manage_pet as manage_pet
from controllers.manage_pet_controller import ManagePetController
import views.camera_view as camera_view
import views.report_view as report_view
from controllers.report_controller import ReportController
import views.manage_doctor_view as manage_doctor
import views.quanlythuoc_view as quanlythuoc
from views.manage_customer import open_manage_customer_content
from views.medicine_warehouse import open_manage_medicine_content
from views.KeDon_view import open_manage_prescription_content

from views.apppointment_view import open_appointment_content
from views.billing_payment_view import open_invoice_content
from views.disease_treatment_view import open_treatment_content


def show_home_content(frame):
    # Đường dẫn đến hình ảnh
    image_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'home2.jpg')
    
    # Kiểm tra xem file hình ảnh có tồn tại không
    if not os.path.exists(image_path):
        label = ctk.CTkLabel(frame, text="Không tìm thấy hình ảnh! Vui lòng thêm file home_image.jpg vào thư mục images/",
                             font=("Arial", 14), text_color="red")
        label.pack(pady=30)
        return

    # Tải và hiển thị hình ảnh
    image = Image.open(image_path)
    ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(800, 600))  # Điều chỉnh kích thước hình ảnh
    image_label = ctk.CTkLabel(frame, image=ctk_image, text="")  # text="" để không hiển thị chữ trên hình ảnh
    image_label.pack(pady=30)

def create_home_window(root):
    # Clear current content
    for widget in root.winfo_children():
        widget.destroy()

    # Configure window
    root.title("Quản lý Phòng Khám Thú Y")
    root.geometry("1200x650")

    # Sidebar with scrollbar
    sidebar = ctk.CTkScrollableFrame(root, width=250, height=650, corner_radius=0)
    sidebar.pack(side="left", fill="y")
    
    title_label = ctk.CTkLabel(sidebar, text="🐾 MENU", font=("Arial", 20, "bold"))
    title_label.pack(pady=20)

    # Function to change main content
    def set_content(content_func):
        for widget in main_content.winfo_children():
            widget.destroy()
        content_func(main_content)

    # Logout function
    def logout():
        from views.login_view import show_login_content
        for widget in root.winfo_children():
            widget.destroy()
        show_login_content(root, create_home_window)

    # Show report function
    def show_report():
        import views.report_view as report_view
        report_controller = ReportController(main_content)
        report_controller.show_report()

    # Menu buttons
    buttons = [
        ("🏠 Trang chủ", lambda: set_content(show_home_content)),
        ("🐶 Quản lý Thú cưng", lambda: set_content(manage_pet.open_manage_pet_content)),
        ("📊 Báo cáo", lambda: show_report()),
        ("🧑‍⚕️ Quản lý Bác sĩ", lambda: set_content(manage_doctor.open_manage_doctor_content)),
        ("💊 Quản lý Thuốc", lambda: set_content(quanlythuoc.open_manage_drug_content)),
        ("💊Điều trị bệnh", lambda: set_content(open_treatment_content)),
        ("🧾 Thanh toán Hóa đơn", lambda: set_content(open_invoice_content)),
        ("📅 Quản lý Lịch hẹn", lambda: set_content(open_appointment_content)),
        ("👥 Quản lý Khách hàng", lambda: set_content(open_manage_customer_content)),
        ("🏥 Quản lý Kho Thuốc", lambda: set_content(open_manage_medicine_content)),
        ("📷 Nhận diện", lambda: set_content(camera_view.show_camera_content)),
        ("📝 Kê Đơn", lambda: set_content(open_manage_prescription_content)),
        ("🚪 Đăng xuất", logout),

    ]

    for btn_text, command in buttons:
        button = ctk.CTkButton(sidebar, text=btn_text, font=("Arial", 14),
                              corner_radius=10, width=220, height=40,
                              fg_color="#34495E", hover_color="#2C3E50",
                              command=command if command else lambda: print(f"{btn_text} chưa được triển khai"))
        button.pack(pady=8)

    # Main content area
    main_content = ctk.CTkFrame(root, fg_color="white", width=950, height=850)
    main_content.pack(side="right", fill="both", expand=True)

    show_home_content(main_content)
    return root

def open_home():
    root = ctk.CTk()
    create_home_window(root)
    root.mainloop()

if __name__ == "__main__":
    open_home()