import mysql.connector
from utils.connect_dtb import connect_db

def login(username, password, root, open_main_callback):
    try:
        conn = connect_db()  # Kết nối đến database
        cursor = conn.cursor()

        # Kiểm tra tài khoản trong bảng nguoi_dung 
        query = "SELECT * FROM nguoi_dung WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            root.destroy()  # Đóng cửa sổ đăng nhập ngay lập tức
            open_main_callback(root)  # Gọi hàm mở giao diện chính
            return True  # Trả về True nếu đăng nhập thành công
        else:
            return False  # Trả về False nếu đăng nhập thất bại

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        return False  # Trả về False nếu có lỗi kết nối