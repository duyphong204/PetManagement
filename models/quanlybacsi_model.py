import mysql.connector
import re
from tkinter import messagebox

class DoctorModel:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="qlthucung2"
            )
            print("Kết nối CSDL thành công!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối CSDL: {e}")
            self.connection = None

    def validate_doctor_data(self, doctor_data):
        if not doctor_data["Họ tên"]:
            messagebox.showerror("Lỗi", "Họ tên không được để trống")
            return False
        if not re.match("^[A-Za-zÀ-ỹ\s]+$", doctor_data["Họ tên"]):
            messagebox.showerror("Lỗi", "Họ tên chỉ được chứa chữ cái và dấu cách")
            return False
        
        if not doctor_data["Chuyên môn"]:
            messagebox.showerror("Lỗi", "Chuyên môn không được để trống")
            return False
        if not re.match("^[A-Za-zÀ-ỹ\s]+$", doctor_data["Chuyên môn"]):
            messagebox.showerror("Lỗi", "Chuyên môn chỉ được chứa chữ cái và dấu cách")
            return False
        
        phone_number = doctor_data.get("Số điện thoại")
        if not phone_number:
            messagebox.showerror("Lỗi", "Số điện thoại không được để trống")
            return False
        if not phone_number.startswith("0") or not (8 <= len(phone_number) <= 11):
            messagebox.showerror("Lỗi", "Số điện thoại phải bắt đầu bằng '0' và có độ dài từ 8-11 số")
            return False
        
        email = doctor_data.get("Email")
        if not email:
            messagebox.showerror("Lỗi", "Email không được để trống")
            return False
        if "@" not in email or "." not in email:
            messagebox.showerror("Lỗi", "Email phải có chứa dấu '@' và '.'")
            return False

        return True

    def check_doctor_exists(self, doctor_data):
        cursor = self.connection.cursor()

        sql_phone = "SELECT id FROM bac_si WHERE so_dien_thoai = %s"
        cursor.execute(sql_phone, (doctor_data["Số điện thoại"],))
        if cursor.fetchone():
            return "Số điện thoại bác sĩ đã tồn tại"

        sql_email = "SELECT id FROM bac_si WHERE email = %s"
        cursor.execute(sql_email, (doctor_data["Email"],))
        if cursor.fetchone():
            return "Email bác sĩ đã tồn tại"

        return None

    def process_id_nguoi_dung(self, id_value):
        try:
            if id_value == "":
                return None
            return int(id_value)
        except ValueError:
            messagebox.showerror("Lỗi", "ID Người dùng phải là số nguyên.")
            return None

    def get_next_available_id(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM bac_si ORDER BY id ASC")
        used_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()

        if not used_ids or used_ids[0] != 1:
            return 1

        for i in range(1, len(used_ids) + 2):
            if i not in used_ids:
                return i

    def add_doctor(self, doctor_data):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return False

        if self.validate_doctor_data(doctor_data):
            error = self.check_doctor_exists(doctor_data)
            if error:
                messagebox.showerror("Lỗi", error)
                return False

            id_nguoi_dung = self.process_id_nguoi_dung(doctor_data.get("ID Người Dùng"))
            if id_nguoi_dung is not None:
                cursor = self.connection.cursor()
                cursor.execute("SELECT COUNT(*) FROM bac_si WHERE id_nguoi_dung = %s", (id_nguoi_dung,))
                if cursor.fetchone()[0] > 0:
                    messagebox.showerror("Lỗi", "ID Người dùng đã tồn tại trong bảng bác sĩ")
                    cursor.close()
                    return False
                cursor.execute("SELECT COUNT(*) FROM nguoi_dung WHERE id = %s", (id_nguoi_dung,))
                if cursor.fetchone()[0] == 0:
                    messagebox.showerror("Lỗi", "ID Người dùng không tồn tại trong bảng người dùng")
                    cursor.close()
                    return False
                cursor.close()

            new_id = self.get_next_available_id()
            cursor = self.connection.cursor()
            sql = """
            INSERT INTO bac_si (id, ho_ten, chuyen_mon, so_dien_thoai, email, id_nguoi_dung)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(sql, (
                    new_id,
                    doctor_data["Họ tên"],
                    doctor_data["Chuyên môn"],
                    doctor_data["Số điện thoại"],
                    doctor_data["Email"],
                    id_nguoi_dung
                ))
                self.connection.commit()
                return True
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm bác sĩ: {e}")
                return False
            finally:
                cursor.close()

    def update_doctor(self, doctor_id, doctor_data):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return False

        if not doctor_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn bác sĩ để cập nhật!")
            return False

        if self.validate_doctor_data(doctor_data):
            cursor = self.connection.cursor()
            try:
                id_nguoi_dung = self.process_id_nguoi_dung(doctor_data.get("ID Người Dùng"))
                if id_nguoi_dung is not None:
                    cursor.execute("SELECT COUNT(*) FROM nguoi_dung WHERE id = %s", (id_nguoi_dung,))
                    if cursor.fetchone()[0] == 0:
                        messagebox.showerror("Lỗi", "ID Người dùng không tồn tại trong cơ sở dữ liệu")
                        return False

                sql = """
                UPDATE bac_si
                SET ho_ten = %s, chuyen_mon = %s, so_dien_thoai = %s, email = %s, id_nguoi_dung = %s
                WHERE id = %s
                """
                cursor.execute(sql, (
                    doctor_data["Họ tên"],
                    doctor_data["Chuyên môn"],
                    doctor_data["Số điện thoại"],
                    doctor_data["Email"],
                    id_nguoi_dung,
                    doctor_id
                ))
                self.connection.commit()
                return True
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi cập nhật bác sĩ: {e}")
                return False
            finally:
                cursor.close()

    def delete_doctor(self, doctor_id):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return False
        if not doctor_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn bác sĩ để xóa!")
            return False
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM bac_si WHERE id = %s", (doctor_id,))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa bác sĩ: {e}")
            return False
        finally:
            cursor.close()

    def search_doctors(self, keyword):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return []
        if not keyword:
            return self.get_all_doctors()
        cursor = self.connection.cursor()
        try:
            sql = """
            SELECT id, ho_ten, chuyen_mon, so_dien_thoai, email, id_nguoi_dung
            FROM bac_si 
            WHERE ho_ten LIKE %s OR chuyen_mon LIKE %s OR so_dien_thoai LIKE %s OR email LIKE %s
            """
            pattern = f"%{keyword}%"
            cursor.execute(sql, (pattern, pattern, pattern, pattern))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {e}")
            return []
        finally:
            cursor.close()

    def get_all_doctors(self):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return []
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, ho_ten, chuyen_mon, so_dien_thoai, email, id_nguoi_dung FROM bac_si")
            return cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách bác sĩ: {e}")
            return []
        finally:
            cursor.close()