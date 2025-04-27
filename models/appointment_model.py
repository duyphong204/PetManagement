import mysql.connector
from tkinter import messagebox
from datetime import datetime

class AppointmentModel:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="qlthucung2"
            )
            print("Kết nối cơ sở dữ liệu thành công!")
        except mysql.connector.Error as e:
            messagebox.showwarning("Lỗi kết nối", f"Không thể kết nối đến cơ sở dữ liệu: {e}")

    def validate_appointment_data(self, appointment_data):
        if not appointment_data.get("id_thu_cung"):
            messagebox.showwarning("Cảnh báo", "Thú cưng hẹn không được để trống!")
            return False
        if not appointment_data.get("ngay_hen"):
            messagebox.showwarning("Cảnh báo", "Ngày hẹn không được để trống!")
            return False
        if not appointment_data.get("gio_hen"):
            messagebox.showwarning("Cảnh báo", "Giờ hẹn không được để trống!")
            return False
        if not appointment_data.get("trang_thai"):
            messagebox.showwarning("Cảnh báo", "Trạng thái không được để trống!")
            return False
        if not appointment_data.get("id_bac_si"):
            messagebox.showwarning("Cảnh báo", "Bác sĩ hẹn không được để trống!")
            return False
        return True

    def check_pet_exists(self, pet_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM thu_cung WHERE id = %s", (pet_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def check_doctor_exists(self, doctor_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM bac_si WHERE id = %s", (doctor_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def get_doctors(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, ho_ten FROM bac_si")
            return cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showwarning("Lỗi", f"Lỗi khi lấy danh sách bác sĩ: {e}")
            return []
        finally:
            cursor.close()

    def get_doctor_id_by_name(self, doctor_name):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id FROM bac_si WHERE ho_ten = %s", (doctor_name,))
            result = cursor.fetchone()
            return result[0] if result else None
        except mysql.connector.Error as e:
            messagebox.showwarning("Lỗi", f"Lỗi khi tìm bác sĩ: {e}")
            return None
        finally:
            cursor.close()

    def add_appointment(self, appointment_data):
        if not self.validate_appointment_data(appointment_data):
            return
        if not self.check_pet_exists(appointment_data["id_thu_cung"]):
            messagebox.showwarning("Cảnh báo", f"Thú cưng với ID {appointment_data['id_thu_cung']} không tồn tại!")
            return
        if not self.check_doctor_exists(appointment_data["id_bac_si"]):
            messagebox.showwarning("Cảnh báo", f"Bác sĩ với ID {appointment_data['id_bac_si']} không tồn tại!")
            return
        cursor = self.connection.cursor()
        sql = """
        INSERT INTO lich_hen (id_thu_cung, ngay_hen, gio_hen, trang_thai, id_bac_si)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (
                appointment_data["id_thu_cung"],
                appointment_data["ngay_hen"],
                appointment_data["gio_hen"],
                appointment_data["trang_thai"],
                appointment_data["id_bac_si"]
            ))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Thêm lịch hẹn thành công!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm lịch hẹn: {e}")
        finally:
            cursor.close()

    def delete_appointment(self, id):
        if not id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn lịch hẹn để xóa!")
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM lich_hen WHERE id = %s", (id,))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Xóa lịch hẹn thành công!")
        except mysql.connector.Error as e:
            messagebox.showwarning("Lỗi", f"Lỗi khi xóa lịch hẹn: {e}")
        finally:
            cursor.close()

    def update_appointment(self, appointment_data):
        if not self.validate_appointment_data(appointment_data):
            return
        if not self.check_pet_exists(appointment_data["id_thu_cung"]):
            messagebox.showwarning("Cảnh báo", f"Thú cưng với ID {appointment_data['id_thu_cung']} không tồn tại!")
            return
        if not self.check_doctor_exists(appointment_data["id_bac_si"]):
            messagebox.showwarning("Cảnh báo", f"Bác sĩ với ID {appointment_data['id_bac_si']} không tồn tại!")
            return
        cursor = self.connection.cursor()
        sql = """
        UPDATE lich_hen
        SET id_thu_cung = %s, ngay_hen = %s, gio_hen = %s, trang_thai = %s, id_bac_si = %s
        WHERE id = %s
        """
        try:
            cursor.execute(sql, (
                appointment_data["id_thu_cung"],
                appointment_data["ngay_hen"],
                appointment_data["gio_hen"],
                appointment_data["trang_thai"],
                appointment_data["id_bac_si"],
                appointment_data["id"]
            ))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Cập nhật lịch hẹn thành công!")
        except mysql.connector.Error as e:
            messagebox.showwarning("Lỗi", f"Lỗi khi cập nhật lịch hẹn: {e}")
        finally:
            cursor.close()

    def get_all_appointments(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                SELECT lh.id, lh.id_thu_cung, tc.ten AS ten_thu_cung, cs.ho_ten AS ten_chu_so_huu, lh.ngay_hen, lh.gio_hen, lh.trang_thai, bs.ho_ten AS ten_bac_si
                FROM lich_hen lh
                JOIN thu_cung tc ON lh.id_thu_cung = tc.id
                JOIN chu_so_huu cs ON tc.id_chu_so_huu = cs.id
                JOIN bac_si bs ON lh.id_bac_si = bs.id
            """)
            appointments = cursor.fetchall()
            if not appointments:
                # Kiểm tra lý do không có dữ liệu
                cursor.execute("SELECT COUNT(*) FROM lich_hen")
                lich_hen_count = cursor.fetchone()[0]
                if lich_hen_count == 0:
                    messagebox.showinfo("Thông báo", "Không có dữ liệu lịch hẹn trong CSDL!")
                else:
                    messagebox.showwarning("Cảnh báo", "Dữ liệu không nhất quán! Vui lòng kiểm tra các bảng liên quan (thú cưng, chủ sở hữu, bác sĩ).")
            return appointments
        except mysql.connector.Error as e:
            messagebox.showwarning("Lỗi", f"Lỗi khi lấy danh sách: {e}")
            return []
        finally:
            cursor.close()

    def delete_all_appointments(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM lich_hen")
            self.connection.commit()
            messagebox.showinfo("Thành công", "Đã xóa tất cả lịch hẹn!")
        except mysql.connector.Error as e:
            messagebox.showwarning("Lỗi", f"Lỗi khi xóa tất cả: {e}")
        finally:
            cursor.close()

    def search_appointments(self, conditions):
        """
        Tìm kiếm lịch hẹn theo ngày và từ khóa.
        Nếu bất kỳ trường nào khớp với từ khóa hoặc nằm trong khoảng ngày, kết quả sẽ được trả về.
        """
        if not conditions:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ít nhất một điều kiện tìm kiếm!")
            return []

        cursor = self.connection.cursor(dictionary=True)
        try:
            sql = """
                SELECT 
                    lh.id, 
                    lh.id_thu_cung,
                    tc.ten AS ten_thu_cung, 
                    cs.ho_ten AS ten_chu_so_huu, 
                    lh.ngay_hen, 
                    lh.gio_hen,
                    lh.trang_thai, 
                    bs.ho_ten AS ten_bac_si
                FROM lich_hen lh
                JOIN thu_cung tc ON lh.id_thu_cung = tc.id
                JOIN chu_so_huu cs ON tc.id_chu_so_huu = cs.id
                JOIN bac_si bs ON lh.id_bac_si = bs.id
                WHERE 1=1
            """
            params = []

            # Thêm điều kiện tìm kiếm theo ngày
            if "ngay_hen >=" in conditions and conditions["ngay_hen >="]:
                sql += " AND lh.ngay_hen >= %s"
                params.append(conditions["ngay_hen >="])
            if "ngay_hen <=" in conditions and conditions["ngay_hen <="]:
                sql += " AND lh.ngay_hen <= %s"
                params.append(conditions["ngay_hen <="])

            # Thêm điều kiện tìm kiếm theo từ khóa
            if "keyword" in conditions and conditions["keyword"]:
                keyword = f"%{conditions['keyword']}%"
                sql += """
                    AND (
                        CAST(lh.id AS CHAR) LIKE %s OR
                        tc.ten LIKE %s OR
                        cs.ho_ten LIKE %s OR
                        lh.trang_thai LIKE %s OR
                        bs.ho_ten LIKE %s
                    )
                """
                params.extend([keyword, keyword, keyword, keyword, keyword])

            sql += " ORDER BY lh.ngay_hen DESC"

            # Debug thông tin truy vấn
            print("SQL Query:", sql)
            print("Parameters:", params)

            cursor.execute(sql, tuple(params))
            results = cursor.fetchall()

            if not results:
                messagebox.showinfo("Thông báo", "Không tìm thấy kết quả phù hợp")
            return results
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi database: {str(e)}")
            return []
        finally:
            cursor.close()