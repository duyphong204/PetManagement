import mysql.connector
from utils.connect_dtb import connect_db

class UserModel:
    def __init__(self):
        # Không cần truyền db_config nữa, sẽ dùng connect_db() từ utils/connectdb.py
        pass

    def get_user_info(self, user_id):
        """ Lấy thông tin cá nhân của người dùng từ database. """
        connection = connect_db()
        if not connection:
            print("Không thể kết nối đến cơ sở dữ liệu.")
            return None

        cursor = connection.cursor(dictionary=True)

        query = "SELECT id, ho_ten, so_dien_thoai, email, dia_chi FROM chu_so_huu WHERE id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result if result else None

    def get_appointments_info(self, user_id):
        """ Lấy thông tin các lịch hẹn của người dùng từ database. """
        connection = connect_db()
        if not connection:
            print("Không thể kết nối đến cơ sở dữ liệu.")
            return None

        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT l.id, l.ngay_hen, l.gio_hen, l.id_thu_cung, l.id_bac_si, l.trang_thai
        FROM lich_hen l
        JOIN thu_cung k ON l.id_thu_cung = k.id
        JOIN chu_so_huu s ON k.id_chu_so_huu = s.id
        WHERE s.id = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return result if result else None

    def get_user_owner_id(self, user_id):
        """Lấy owner_id từ cơ sở dữ liệu theo user_id"""
        connection = connect_db()
        if not connection:
            print("Không thể kết nối đến cơ sở dữ liệu.")
            return None

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

# Chạy thử
if __name__ == "__main__":
    # Tạo instance của UserModel và thử lấy thông tin
    user_model = UserModel()

    # Thử lấy thông tin người dùng với user_id (thay 1 bằng ID thực tế trong database của bạn)
    user_info = user_model.get_user_info(1)
    print("Thông tin người dùng:", user_info)

    # Thử lấy thông tin lịch hẹn
    appointments = user_model.get_appointments_info(1)
    print("Thông tin lịch hẹn:", appointments)

    # Thử lấy owner_id
    owner_id = user_model.get_user_owner_id(1)
    print("Owner ID:", owner_id)