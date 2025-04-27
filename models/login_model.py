
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
            # Kết nối đến cơ sở dữ liệu
            conn = connect_db()
            cursor = conn.cursor(dictionary=True)  # Dùng dictionary để trả về dữ liệu dưới dạng từ điển

            # Truy vấn để lấy thông tin người dùng theo username và password
            query = "SELECT id, username, role, password FROM nguoi_dung WHERE username = %s"
            cursor.execute(query, (username,))  # Chỉ truyền username để lấy thông tin người dùng
            user = cursor.fetchone()  # Lấy kết quả tìm kiếm đầu tiên

            cursor.close()  # Đóng con trỏ sau khi xong
            conn.close()  # Đóng kết nối sau khi xong

            if user:
                # So sánh mật khẩu đã mã hóa (nên sử dụng hàm hash mật khẩu thực tế như bcrypt, hash, v.v)
                if user["password"] == password:
                    return user, ""  # Trả về dữ liệu người dùng (id, username, role)
                else:
                    return None, "Mật khẩu không đúng!"  # Nếu mật khẩu không khớp
            else:
                return None, "Tên đăng nhập không chính xác!"  # Nếu không tìm thấy người dùng
        
        except mysql.connector.Error as e:
            return None, f"Lỗi kết nối CSDL: {e}"