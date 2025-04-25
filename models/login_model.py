import mysql.connector
from utils.connect_dtb import connect_db

class LoginModel:
    def __init__(self):
        """Khởi tạo kết nối cơ sở dữ liệu."""
        self.conn = connect_db()
        self.cursor = self.conn.cursor()

    def validate_login_data(self, username: str, password: str) -> tuple[bool, str]:
        """Kiểm tra dữ liệu đầu vào."""
        if not username or not password:
            return False, "Tên đăng nhập hoặc mật khẩu không được để trống!"
        return True, ""

    def check_credentials(self, username: str, password: str) -> tuple[bool, str]:
        """Kiểm tra thông tin đăng nhập trong cơ sở dữ liệu."""
        try:
            query = "SELECT * FROM nguoi_dung WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            user = self.cursor.fetchone()
            return bool(user), ""
        except mysql.connector.Error as e:
            return False, f"Lỗi kết nối CSDL: {e}"

    def close_connection(self) -> None:
        """Đóng kết nối cơ sở dữ liệu."""
        if self.cursor:
            self.cursor.close()
        if self.conn and self.conn.is_connected():
            self.conn.close()