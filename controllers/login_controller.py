from models.login_model import LoginModel

class LoginController:
    def __init__(self):
        self.model = LoginModel()

    def login(self, username, password, open_main_callback):
        """Xử lý logic đăng nhập"""
        is_valid, message = self.model.validate_login_data(username, password)
        if not is_valid:
            return False, message

        is_valid, message = self.model.check_credentials(username, password)
        if is_valid:
            open_main_callback()  # Mở giao diện menu
            return True, "Đăng nhập thành công!"
        return False, message or "Tên đăng nhập hoặc mật khẩu không chính xác!"