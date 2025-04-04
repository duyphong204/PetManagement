"""
from models.login_model import LoginModel

class LoginController:
    def __init__(self):
        self.model = LoginModel()

    def login(self, username, password, open_main_callback):
        # Xử lý logic đăng nhập
        is_valid, message = self.model.validate_login_data(username, password)
        if not is_valid:
            return False, message

        is_valid, message = self.model.check_credentials(username, password)
        if is_valid:
            open_main_callback()  # Mở giao diện menu
            return True, "Đăng nhập thành công!"
        return False, message or "Tên đăng nhập hoặc mật khẩu không chính xác!"
        """

from models.login_model import LoginModel
from views.admin_view import open_admin_dashboard
from views.doctor_view import open_doctor_dashboard
from views.user_view import open_user_dashboard
from tkinter import messagebox

class LoginController:
    def __init__(self, root):
        self.root = root
        self.model = LoginModel()

    def login(self, username, password, open_home_callback):
        """Xử lý logic đăng nhập"""
        # Kiểm tra dữ liệu đầu vào
        is_valid, message = self.model.validate_login_data(username, password)
        if not is_valid:
            messagebox.showerror("Lỗi", message)
            return False, message # Trả về tuple (False, message)


        # Kiểm tra thông tin đăng nhập
        user_data, message = self.model.check_credentials(username, password)
        if not user_data:
            messagebox.showerror("Lỗi", message)
            return False, message  # Trả về tuple (False, message)


        # Đăng nhập thành công, xác thực vai trò và mở giao diện tương ứng
       # self.root.destroy()  # Đóng cửa sổ đăng nhập
        if self.root.winfo_exists():  # Kiểm tra nếu cửa sổ còn tồn tại
            self.root.destroy()
       
        # Xử lý dựa trên vai trò người dùng
        if user_data["role"] == "admin":
            open_admin_dashboard()
        elif user_data["role"] == "bac_si":
            open_doctor_dashboard()
        elif user_data["role"] == "khach_hang":
            open_user_dashboard(user_data["id"])  # Truyền ID người dùng cho giao diện khách hàng
        else:
            messagebox.showerror("Lỗi", "Vai trò người dùng không hợp lệ!")
            return False, message  # Trả về tuple (False, message)


        messagebox.showinfo("Đăng nhập thành công", f"Chào mừng {user_data['username']}!")
        return True, "Đăng nhập thành công"  # Trả về tuple (True, success message)