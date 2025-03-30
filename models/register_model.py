# models/register_model.py
import mysql.connector
import re
from utils.connect_dtb import connect_db

class RegisterModel:
    def __init__(self):
        pass

    def validate_register_data(self, username, password, confirm_password, email):
        """Validate dữ liệu đầu vào"""
        # Kiểm tra username
        if not username or len(username) < 3:
            return False, "Username phải có ít nhất 3 ký tự!"
        if not re.match("^[a-zA-Z0-9_]+$", username):
            return False, "Username chỉ được chứa chữ cái, số và dấu gạch dưới!"

        # Kiểm tra password
        if not password or len(password) < 6:
            return False, "Password phải có ít nhất 6 ký tự!"
        if password != confirm_password:
            return False, "Password và Confirm Password không khớp!"

        # Kiểm tra email
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not email or not re.match(email_pattern, email):
            return False, "Email không hợp lệ!"

        return True, "Dữ liệu hợp lệ"

    def check_username_exists(self, username):
        """Kiểm tra username đã tồn tại chưa"""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM nguoi_dung WHERE username = %s"
            cursor.execute(query, (username,))
            return cursor.fetchone() is not None, "Username đã tồn tại!"
        except mysql.connector.Error as e:
            return True, f"Lỗi khi kiểm tra username: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    def check_email_exists(self, email):
        """Kiểm tra email đã tồn tại chưa"""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            query = "SELECT * FROM nguoi_dung WHERE email = %s"
            cursor.execute(query, (email,))
            return cursor.fetchone() is not None, "Email đã tồn tại!"
        except mysql.connector.Error as e:
            return True, f"Lỗi khi kiểm tra email: {str(e)}"
        finally:
            cursor.close()
            conn.close()

    def insert_user(self, username, password, email):
        """Thêm user mới vào database"""
        conn = connect_db()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO nguoi_dung (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, password, email))
            conn.commit()
            return True, "Đăng ký thành công!"
        except mysql.connector.Error as e:
            return False, f"Lỗi khi thêm user: {str(e)}"
        finally:
            cursor.close()
            conn.close()