from views.main_view import create_home_window
from views.doctor_view import open_doctor_dashboard
from views.user_view import open_user_dashboard

def open_dashboard(login_controller, root):
    # Lấy thông tin vai trò và dữ liệu người dùng từ login_controller
    role = login_controller.role
    user_data = login_controller.user_data

    # Kiểm tra vai trò của người dùng và mở giao diện tương ứng
    if role == "admin":
        create_home_window(root) 
    elif role == "bac_si":
        open_doctor_dashboard(root)  
    elif role == "khach_hang":
        open_user_dashboard(root, user_data["id"])  
    else:
        print("Lỗi: Vai trò người dùng không hợp lệ!")

        