
from models.login_model import LoginModel
from views.main_view import create_home_window
from views.doctor_view import open_doctor_dashboard
from views.user_view import open_user_dashboard
from tkinter import messagebox

class LoginController:
    def __init__(self, root):
        self.root = root
        self.model = LoginModel()
        self.role = None
        self.user_data = None

    def login(self, username, password, open_main_callback=None):
        # Kiểm tra dữ liệu đầu vào
        is_valid, message = self.model.validate_login_data(username, password)
        if not is_valid:
            messagebox.showerror("Lỗi", message)
            return False, message

        # Kiểm tra thông tin đăng nhập
        user_data, message = self.model.check_credentials(username, password)
        if not user_data:
            messagebox.showerror("Lỗi", message)
            return False, message

        # Lưu thông tin người dùng
        self.role = user_data["role"]
        self.user_data = user_data

        # Hiển thị giao diện phù hợp
        self.redirect_to_dashboard()
        messagebox.showinfo("Đăng nhập thành công", f"Chào mừng {user_data['username']}!")
        return True, "Đăng nhập thành công"

    def redirect_to_dashboard(self):
        if self.role == "admin":
            create_home_window(self.root)
        elif self.role == "bac_si":
            open_doctor_dashboard(self.root)
        elif self.role == "khach_hang":
            open_user_dashboard(self.root, self.user_data["id"])
        else:
            messagebox.showerror("Lỗi", "Vai trò người dùng không hợp lệ!")