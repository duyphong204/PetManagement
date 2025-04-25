from models.login_model import LoginModel

class LoginController:
    def __init__(self):
        self.model = LoginModel()

    def login(self, username: str, password: str, open_main_callback) -> tuple[bool, str]:
        """Xử lý logic đăng nhập."""
        # Kiểm tra dữ liệu đầu vào
        if not (is_valid := self.model.validate_login_data(username, password))[0]:
            return is_valid

        # Kiểm tra thông tin đăng nhập
        is_valid, message = self.model.check_credentials(username, password)
        if is_valid:
            open_main_callback()  # Mở giao diện chính
            return True, "Đăng nhập thành công!"
        return False, message or "Tên đăng nhập hoặc mật khẩu không chính xác!"

    def close(self) -> None:
        """Đóng tài nguyên, ví dụ: kết nối cơ sở dữ liệu."""
        self.model.close_connection()