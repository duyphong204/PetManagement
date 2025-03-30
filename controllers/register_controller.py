# controllers/register_controller.py
from models.register_model import RegisterModel

class RegisterController:
    def __init__(self):
        self.model = RegisterModel()

    def register(self, username, password, confirm_password, email, open_login_callback):
        """Xử lý logic đăng ký"""
        # Bước 1: Validate dữ liệu đầu vào
        is_valid, message = self.model.validate_register_data(username, password, confirm_password, email)
        if not is_valid:
            return False, message

        # Bước 2: Kiểm tra username đã tồn tại chưa
        exists, message = self.model.check_username_exists(username)
        if exists:
            return False, message

        # Bước 3: Kiểm tra email đã tồn tại chưa
        exists, message = self.model.check_email_exists(email)
        if exists:
            return False, message

        # Bước 4: Thêm user vào database
        is_valid, message = self.model.insert_user(username, password, email)
        if is_valid:
            open_login_callback()  # Mở giao diện đăng nhập
            return True, "Đăng ký thành công!"
        return False, message or "Đăng ký thất bại!"