import mysql.connector
from utils.connect_dtb import connect_db  # Giả sử bạn có một file connect_dtb.py chứa thông tin kết nối

class UserModel:
    def __init__(self):
        """Khởi tạo UserModel mà không cần truyền tham số kết nối"""
        pass

    def connect(self):
        """Tạo kết nối với cơ sở dữ liệu"""
        return connect_db()  # Gọi hàm connect_db để lấy kết nối

    def get_user_info(self, user_id):
        """Lấy thông tin cá nhân của người dùng từ database."""
        connection = self.connect()  # Gọi connect để kết nối DB
        cursor = connection.cursor(dictionary=True)

        query = "SELECT id, ho_ten, so_dien_thoai, email, dia_chi FROM chu_so_huu WHERE id_nguoi_dung = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result if result else None

    def get_appointments_info(self, user_id):
        """Lấy thông tin các lịch hẹn của người dùng từ database."""
        connection = self.connect()  # Gọi connect để kết nối DB
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT l.id, l.ngay_hen, l.gio_hen, l.id_thu_cung, l.id_bac_si, l.trang_thai
        FROM lich_hen l
        JOIN thu_cung k ON l.id_thu_cung = k.id
        JOIN chu_so_huu s ON k.id_chu_so_huu = s.id
        WHERE s.id_nguoi_dung = %s
        """
        cursor.execute(query, (user_id,))
        appointments = cursor.fetchall()

        cursor.close()
        connection.close()

        return appointments if appointments else []

    def get_user_owner_id(self, user_id):
        """Lấy owner_id từ cơ sở dữ liệu theo user_id."""
        connection = self.connect()  # Gọi connect để kết nối DB
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id FROM chu_so_huu WHERE id_nguoi_dung = %s", (user_id,))
            result = cursor.fetchone()
            if result:
                return result["id"]
            else:
                return None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        finally:
            cursor.close()
            connection.close()

    def check_duplicate_appointment(self, ngay_hen, gio_hen, id_bac_si):
        """Kiểm tra lịch hẹn có bị trùng với bác sĩ không."""
        try:
            connection = self.connect()  # Gọi connect để kết nối DB
            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT * FROM lich_hen
            WHERE id_bac_si = %s AND ngay_hen = %s AND gio_hen = %s AND trang_thai != 'Đã hủy' 
            """
            cursor.execute(query, (id_bac_si, ngay_hen, gio_hen))
            result = cursor.fetchone()

            return True if result else False

        except mysql.connector.Error as e:
            print(f"Lỗi trong khi kiểm tra trùng lịch: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

    def save_appointment(self, ngay_hen, gio_hen, id_thu_cung, id_bac_si):
        """Lưu lịch hẹn vào cơ sở dữ liệu và trả về ID vừa tạo."""
        try:
            connection = self.connect()  # Gọi connect để kết nối DB
            cursor = connection.cursor()

            insert_query = """
            INSERT INTO lich_hen (ngay_hen, gio_hen, id_thu_cung, id_bac_si, trang_thai)
            VALUES (%s, %s, %s, %s, 'Chờ xác nhận')
            """
            cursor.execute(insert_query, (ngay_hen, gio_hen, id_thu_cung, id_bac_si))
            connection.commit()

            new_id = cursor.lastrowid  # Lấy ID tự động mới được sinh ra
            return new_id

        except mysql.connector.Error as e:
            print(f"Lỗi khi lưu lịch hẹn: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

    def is_time_slot_available(self, ngay_hen, gio_hen):
        """Kiểm tra thời gian đặt lịch có cách đủ 30 phút với các lịch đã có trong cùng ngày và cùng bác sĩ."""
        connection = self.connect()  # Gọi connect để kết nối DB
        cursor = connection.cursor()

        query = """
        SELECT *
        FROM lich_hen
        WHERE DATE(ngay_hen) = %s
        AND ABS(TIMESTAMPDIFF(MINUTE, CONCAT(ngay_hen, ' ', gio_hen), %s)) < 30
        """

        gio_full = f"{ngay_hen} {gio_hen}:00"
        cursor.execute(query, (ngay_hen, gio_full))
        result = cursor.fetchone()

        return result is None  # True nếu không có lịch trùng

    def get_pets_by_user(self, user_id):
        """Lấy danh sách thú cưng của người dùng từ cơ sở dữ liệu."""
        connection = self.connect()  # Gọi connect để kết nối DB
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT k.id, k.ten, k.loai, k.gioi_tinh
        FROM thu_cung k
        INNER JOIN chu_so_huu s ON s.id = k.id_chu_so_huu
        WHERE s.id_nguoi_dung = %s
        """

        cursor.execute(query, (user_id,))
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return result if result else None

    def get_doctors(self):
        """Lấy danh sách bác sĩ từ cơ sở dữ liệu."""
        connection = self.connect()  # Gọi connect để kết nối DB
        cursor = connection.cursor(dictionary=True)

        query = "SELECT id, ho_ten FROM bac_si"
        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return result if result else []

    def delete_appointment(self, appointment_id):
        """Xóa lịch hẹn của người dùng."""
        try:
            connection = self.connect()  # Gọi connect để kết nối DB
            cursor = connection.cursor(dictionary=True)

            query = "DELETE FROM lich_hen WHERE id = %s"
            cursor.execute(query, (appointment_id,))
            connection.commit()

            cursor.close()
            connection.close()

            return {"success": True, "message": "Lịch hẹn đã được xóa thành công."}

        except Exception as e:
            return {"success": False, "message": f"Đã xảy ra lỗi: {e}"}

    def search_appointments(self, user_id, tu_ngay, den_ngay):
        """Tìm kiếm các lịch hẹn trong khoảng thời gian nhất định."""
        try:
            connection = self.connect()  # Gọi connect để kết nối DB
            cursor = connection.cursor(dictionary=True)

            query = """
            SELECT l.id, l.ngay_hen, l.gio_hen, l.id_thu_cung, l.id_bac_si, l.trang_thai
            FROM lich_hen l
            JOIN thu_cung k ON l.id_thu_cung = k.id
            JOIN chu_so_huu s ON k.id_chu_so_huu = s.id
            WHERE s.id_nguoi_dung = %s
            AND l.ngay_hen BETWEEN %s AND %s
            """
            cursor.execute(query, (user_id, tu_ngay, den_ngay))
            results = cursor.fetchall()

            cursor.close()
            connection.close()

            return results if results else []

        except Exception as e:
            print("Lỗi tìm kiếm lịch hẹn:", e)
            return []
