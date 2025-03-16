import mysql.connector
from utils.connect_dtb import connect_db

class LoginModel:
    def validate_login_data(self, username, password):
        if not username or not password:
            return False, "Tên đăng nhập hoặc mật khẩu không được để trống!"
        return True, ""

    def check_credentials(self, username, password):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = "SELECT * FROM nguoi_dung WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            return user is not None, ""
        except mysql.connector.Error as e:
            return False, f"Lỗi kết nối CSDL: {e}"