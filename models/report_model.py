from utils.connect_dtb import connect_db

class ReportModel:
    def __init__(self):
        self.db_connection = connect_db()

    def get_total_revenue(self, start_date=None, end_date=None):
        if not self.db_connection or not self.db_connection.is_connected():
            return None, "Không thể kết nối đến cơ sở dữ liệu!"
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT SUM(tong_tien) FROM hoa_don"
            params = ()
            if start_date and end_date:
                query += " WHERE ngay_tao BETWEEN %s AND %s"
                params = (start_date, end_date)
            cursor.execute(query, params)
            total = cursor.fetchone()[0] or 0
            cursor.close()
            return total, None
        except Exception as e:
            if cursor: cursor.close()
            return None, f"Lỗi truy vấn: {e}"

    def get_revenue_details(self, start_date=None, end_date=None):
        if not self.db_connection or not self.db_connection.is_connected():
            return None, "Không thể kết nối đến cơ sở dữ liệu!"
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT id, ngay_tao, tong_tien, trang_thai FROM hoa_don"
            params = ()
            if start_date and end_date:
                query += " WHERE ngay_tao BETWEEN %s AND %s"
                params = (start_date, end_date)
            cursor.execute(query, params)
            details = cursor.fetchall()
            cursor.close()
            return details, None
        except Exception as e:
            if cursor: cursor.close()
            return None, f"Lỗi truy vấn: {e}"

    def get_revenue_by_date(self, start_date=None, end_date=None):
        if not self.db_connection or not self.db_connection.is_connected():
            return None, "Không thể kết nối đến cơ sở dữ liệu!"
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT DATE(ngay_tao), SUM(tong_tien) FROM hoa_don"
            params = ()
            if start_date and end_date:
                query += " WHERE ngay_tao BETWEEN %s AND %s"
                params = (start_date, end_date)
            query += " GROUP BY DATE(ngay_tao)"
            cursor.execute(query, params)
            data = cursor.fetchall()
            cursor.close()
            return data, None
        except Exception as e:
            if cursor: cursor.close()
            return None, f"Lỗi truy vấn: {e}"

    def get_appointment_stats(self, start_date=None, end_date=None):
        if not self.db_connection or not self.db_connection.is_connected():
            return None, "Không thể kết nối đến cơ sở dữ liệu!"
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT trang_thai, COUNT(*) FROM lich_hen"
            params = ()
            if start_date and end_date:
                query += " WHERE ngay_hen BETWEEN %s AND %s"
                params = (start_date, end_date)
            query += " GROUP BY trang_thai"
            cursor.execute(query, params)
            stats = {"Chờ xác nhận": 0, "Đã xác nhận": 0, "Đã hoàn thành": 0, "Đã hủy": 0}
            for row in cursor.fetchall():
                stats[row[0]] = row[1]
            cursor.close()
            return stats, None
        except Exception as e:
            if cursor: cursor.close()
            return None, f"Lỗi truy vấn: {e}"

    def get_appointment_details(self, start_date=None, end_date=None):
        if not self.db_connection or not self.db_connection.is_connected():
            return None, "Không thể kết nối đến cơ sở dữ liệu!"
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT lh.id, lh.ngay_hen, lh.gio_hen, tc.ten, bs.ho_ten, lh.trang_thai
                FROM lich_hen lh
                JOIN thu_cung tc ON lh.id_thu_cung = tc.id
                JOIN bac_si bs ON lh.id_bac_si = bs.id
            """
            params = ()
            if start_date and end_date:
                query += " WHERE lh.ngay_hen BETWEEN %s AND %s"
                params = (start_date, end_date)
            cursor.execute(query, params)
            details = cursor.fetchall()
            cursor.close()
            return details, None
        except Exception as e:
            if cursor: cursor.close()
            return None, f"Lỗi truy vấn: {e}"

    def get_pet_stats(self):
        if not self.db_connection or not self.db_connection.is_connected():
            return None, "Không thể kết nối đến cơ sở dữ liệu!"
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT loai, COUNT(*) FROM thu_cung GROUP BY loai"
            cursor.execute(query)
            stats = cursor.fetchall()
            cursor.close()
            return stats, None
        except Exception as e:
            if cursor: cursor.close()
            return None, f"Lỗi truy vấn: {e}"

    def get_pet_details(self):
        if not self.db_connection or not self.db_connection.is_connected():
            return None, "Không thể kết nối đến cơ sở dữ liệu!"
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT tc.ten, tc.loai, tc.tuoi, tc.gioi_tinh, cs.ho_ten
                FROM thu_cung tc
                JOIN chu_so_huu cs ON tc.id_chu_so_huu = cs.id
            """
            cursor.execute(query)
            details = cursor.fetchall()
            cursor.close()
            return details, None
        except Exception as e:
            if cursor: cursor.close()
            return None, f"Lỗi truy vấn: {e}"

    def get_inventory_stats(self):
        if not self.db_connection or not self.db_connection.is_connected():
            return None, "Không thể kết nối đến cơ sở dữ liệu!"
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT SUM(so_luong) FROM kho_thuoc"
            cursor.execute(query)
            total = cursor.fetchone()[0] or 0

            query = """
                SELECT COUNT(*) 
                FROM kho_thuoc 
                WHERE han_su_dung <= DATE_ADD(CURDATE(), INTERVAL 30 DAY)
            """
            cursor.execute(query)
            expiring = cursor.fetchone()[0] or 0
            cursor.close()
            return (total, expiring), None
        except Exception as e:
            if cursor: cursor.close()
            return None, f"Lỗi truy vấn: {e}"

    def get_inventory_details(self):
        if not self.db_connection or not self.db_connection.is_connected():
            return None, "Không thể kết nối đến cơ sở dữ liệu!"
        try:
            cursor = self.db_connection.cursor()
            query = """
                SELECT t.ten_thuoc, kt.so_luong, kt.ngay_nhap, kt.han_su_dung
                FROM kho_thuoc kt
                JOIN thuoc t ON kt.id_thuoc = t.id
            """
            cursor.execute(query)
            details = cursor.fetchall()
            cursor.close()
            return details, None
        except Exception as e:
            if cursor: cursor.close()
            return None, f"Lỗi truy vấn: {e}"

    def close_connection(self):
        if self.db_connection and self.db_connection.is_connected():
            self.db_connection.close()