from controllers.login_controller import login
from tkinter import messagebox

class LoginModel:
    def validate_login_data(self, username, password):
        """Kiểm tra dữ liệu đăng nhập trước khi gọi tầng dữ liệu"""
        if username == '' or password == '':
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không được để trống!")
            return False
        # Thêm các kiểm tra khác nếu cần (ví dụ: độ dài mật khẩu, ký tự đặc biệt, v.v.)
        return True

    def login(self, username, password, root, open_main_callback):
        """Xử lý đăng nhập"""
        if self.validate_login_data(username, password):
            # Gọi tầng dữ liệu để kiểm tra thông tin đăng nhập
            return login(username, password, root, open_main_callback)
        return False