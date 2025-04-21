from utils.connect_dtb import connect_db
from datetime import datetime, timedelta

class ReportModel:
    def __init__(self):
        self.connection = connect_db()
        if not self.connection:
            raise Exception("Không thể kết nối cơ sở dữ liệu!")

    def get_pet_statistics(self):
        """Get total number of pets in the system."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT COUNT(*) AS total FROM thu_cung")
            total_pets = cursor.fetchone()["total"]

            cursor.execute("SELECT loai, COUNT(*) AS count FROM thu_cung GROUP BY loai")
            pets_by_type = cursor.fetchall()

            return {"Tổng số thú cưng": total_pets, "Thú cưng theo loại": pets_by_type}
        except Exception as e:
            print(f"Lỗi khi thống kê thú cưng: {e}")
            return {}
        finally:
            cursor.close()

    def get_pet_by_date(self):
        """Get pet statistics by date (month)."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT DATE_FORMAT(ngay_tao, '%Y-%m') AS month, loai, COUNT(*) AS count 
                FROM thu_cung 
                GROUP BY DATE_FORMAT(ngay_tao, '%Y-%m'), loai
                ORDER BY month
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi thống kê thú cưng theo ngày: {e}")
            return []
        finally:
            cursor.close()

    def get_pet_by_owner(self):
        """Get pet statistics by owner."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT c.ho_ten AS owner_name, COUNT(t.id) AS pet_count 
                FROM chu_so_huu c 
                LEFT JOIN thu_cung t ON c.id = t.id_chu_so_huu 
                GROUP BY c.id, c.ho_ten
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi thống kê thú cưng theo chủ sở hữu: {e}")
            return []
        finally:
            cursor.close()

    def get_appointment_statistics(self):
        """Get appointment statistics."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT COUNT(*) AS total FROM lich_hen")
            total_appointments = cursor.fetchone()["total"]

            cursor.execute("SELECT COUNT(*) AS confirmed FROM lich_hen WHERE trang_thai = 'Đã xác nhận'")
            confirmed_appointments = cursor.fetchone()["confirmed"]

            return {
                "Tổng số lịch hẹn": total_appointments,
                "Lịch hẹn đã xác nhận": confirmed_appointments,
                "Lịch hẹn chưa xác nhận": total_appointments - confirmed_appointments,
            }
        except Exception as e:
            print(f"Lỗi khi thống kê lịch hẹn: {e}")
            return {}
        finally:
            cursor.close()

    def get_appointment_by_date(self):
        """Get appointment statistics by date (day and month)."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT DATE_FORMAT(ngay_hen, '%Y-%m-%d') AS day, trang_thai, COUNT(*) AS count 
                FROM lich_hen 
                GROUP BY DATE_FORMAT(ngay_hen, '%Y-%m-%d'), trang_thai
                ORDER BY day
            """)
            appt_by_day = cursor.fetchall()

            cursor.execute("""
                SELECT DATE_FORMAT(ngay_hen, '%Y-%m') AS month, trang_thai, COUNT(*) AS count 
                FROM lich_hen 
                GROUP BY DATE_FORMAT(ngay_hen, '%Y-%m'), trang_thai
                ORDER BY month
            """)
            appt_by_month = cursor.fetchall()

            return {"Theo ngày": appt_by_day, "Theo tháng": appt_by_month}
        except Exception as e:
            print(f"Lỗi khi thống kê lịch hẹn theo ngày: {e}")
            return {"Theo ngày": [], "Theo tháng": []}
        finally:
            cursor.close()

    def get_doctor_statistics(self):
        """Get doctor statistics (specialization)."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT ho_ten, chuyen_mon FROM bac_si")
            doctors = cursor.fetchall()

            cursor.execute("""
                SELECT b.ho_ten, COUNT(d.id) AS treatment_count 
                FROM bac_si b 
                LEFT JOIN dieu_tri d ON b.id = d.id_bac_si 
                GROUP BY b.id, b.ho_ten
            """)
            treatments = cursor.fetchall()

            return {"Bác sĩ và chuyên môn": doctors, "Số ca điều trị theo bác sĩ": treatments}
        except Exception as e:
            print(f"Lỗi khi thống kê bác sĩ: {e}")
            return {"Bác sĩ và chuyên môn": [], "Số ca điều trị theo bác sĩ": []}
        finally:
            cursor.close()

    def get_revenue_statistics(self):
        """Get revenue statistics by month."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT DATE_FORMAT(ngay_tao, '%Y-%m') AS month, SUM(tong_tien) AS total_revenue 
                FROM hoa_don 
                WHERE trang_thai = 'Đã thanh toán'
                GROUP BY DATE_FORMAT(ngay_tao, '%Y-%m')
                ORDER BY month
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi thống kê doanh thu: {e}")
            return []
        finally:
            cursor.close()

    def get_medicine_statistics(self):
        """Get medicine inventory statistics."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT COUNT(*) AS total FROM kho_thuoc")
            total_medicines = cursor.fetchone()["total"]

            cursor.execute("SELECT SUM(so_luong) AS total_quantity FROM kho_thuoc")
            total_quantity = cursor.fetchone()["total_quantity"] or 0

            cursor.execute("SELECT ten_thuoc, so_luong FROM kho_thuoc")
            medicines_by_type = cursor.fetchall()

            expiry_date_threshold = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            cursor.execute("""
                SELECT ten_thuoc, so_luong 
                FROM kho_thuoc 
                WHERE han_su_dung <= %s
            """, (expiry_date_threshold,))
            medicines_near_expiry = cursor.fetchall()

            return {
                "Tổng số loại thuốc": total_medicines,
                "Tổng số lượng thuốc": total_quantity,
                "Thuốc theo loại": medicines_by_type,
                "Thuốc sắp hết hạn": medicines_near_expiry
            }
        except Exception as e:
            print(f"Lỗi khi thống kê kho thuốc: {e}")
            return {
                "Tổng số loại thuốc": 0,
                "Tổng số lượng thuốc": 0,
                "Thuốc theo loại": [],
                "Thuốc sắp hết hạn": []
            }
        finally:
            cursor.close()

    def get_pet_health_statistics(self):
        """Get pet health statistics."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT tinh_trang_suc_khoe, COUNT(*) AS count 
                FROM thu_cung 
                GROUP BY tinh_trang_suc_khoe
            """)
            health_stats = cursor.fetchall()

            cursor.execute("SELECT COUNT(*) AS total FROM thu_cung")
            total_pets = cursor.fetchone()["total"]

            return {
                "Tổng số thú cưng": total_pets,
                "Thú cưng theo tình trạng sức khỏe": health_stats
            }
        except Exception as e:
            print(f"Lỗi khi thống kê sức khỏe thú cưng: {e}")
            return {}
        finally:
            cursor.close()

    def get_pet_health_by_date(self):
        """Get pet health statistics by date (month)."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT DATE_FORMAT(ngay_tao, '%Y-%m') AS month, tinh_trang_suc_khoe, COUNT(*) AS count 
                FROM thu_cung 
                GROUP BY DATE_FORMAT(ngay_tao, '%Y-%m'), tinh_trang_suc_khoe
                ORDER BY month
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi thống kê sức khỏe thú cưng theo ngày: {e}")
            return []
        finally:
            cursor.close()

    def get_pet_health_by_type(self):
        """Get pet health statistics by type."""
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT loai, tinh_trang_suc_khoe, COUNT(*) AS count 
                FROM thu_cung 
                GROUP BY loai, tinh_trang_suc_khoe
            """)
            return cursor.fetchall()
        except Exception as e:
            print(f"Lỗi khi thống kê sức khỏe thú cưng theo loại: {e}")
            return []
        finally:
            cursor.close()

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()