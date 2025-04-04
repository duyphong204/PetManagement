
import mysql.connector
from utils.connect_dtb import connect_db

class LoginModel:
    def validate_login_data(self, username, password):
        """Kiểm tra dữ liệu đầu vào của đăng nhập"""
        if not username or not password:
            return False, "Tên đăng nhập hoặc mật khẩu không được để trống!"
        return True, ""

    def check_credentials(self, username, password):
        """Kiểm tra đăng nhập người dùng"""
        try:
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)  # Dùng dictionary để trả về dữ liệu
            query = "SELECT id, username, role FROM nguoi_dung WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                return user, ""  # Trả về thông tin người dùng (id, username, role)
            else:
                return None, "Tên đăng nhập hoặc mật khẩu không chính xác!"
        except mysql.connector.Error as e:
            return None, f"Lỗi kết nối CSDL: {e}"

