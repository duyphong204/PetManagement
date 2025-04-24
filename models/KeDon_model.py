import mysql.connector
from tkinter import messagebox
from datetime import datetime
import re
from utils.connect_dtb import connect_db

class PrescriptionModel:
    def __init__(self):
        self.connection = connect_db()
        if not self.connection:
            self.connection = None

    def get_appointments(self):
        """Lấy danh sách lịch hẹn chưa được kê đơn"""
        if not self.connection:
            return []
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                SELECT lich_hen.id, thu_cung.ten, bac_si.ho_ten, lich_hen.ngay_hen, lich_hen.gio_hen
                FROM lich_hen
                JOIN thu_cung ON lich_hen.id_thu_cung = thu_cung.id
                JOIN bac_si ON lich_hen.id_bac_si = bac_si.id
                LEFT JOIN ke_don ON lich_hen.id = ke_don.id_lich_hen
                WHERE ke_don.id_lich_hen IS NULL
            """)
            appointments = cursor.fetchall()
            if not appointments:
                messagebox.showinfo("Thông báo", "Không có lịch hẹn nào chưa được kê đơn!")
            return appointments
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách lịch hẹn: {e}")
            return []
        finally:
            cursor.close()

    def get_all_appointments(self):
        """Lấy danh sách tất cả lịch hẹn"""
        if not self.connection:
            return []
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                SELECT lich_hen.id, thu_cung.ten, bac_si.ho_ten, lich_hen.ngay_hen, lich_hen.gio_hen
                FROM lich_hen
                JOIN thu_cung ON lich_hen.id_thu_cung = thu_cung.id
                JOIN bac_si ON lich_hen.id_bac_si = bac_si.id
            """)
            appointments = cursor.fetchall()
            if not appointments:
                messagebox.showinfo("Thông báo", "Không có lịch hẹn nào!")
            return appointments
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách lịch hẹn: {e}")
            return []
        finally:
            cursor.close()

    def get_medicines(self):
        """Lấy danh sách thuốc kèm số lượng trong kho"""
        if not self.connection:
            return []
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                SELECT thuoc.id, thuoc.ten_thuoc, kho_thuoc.so_luong
                FROM thuoc
                LEFT JOIN kho_thuoc ON thuoc.id = kho_thuoc.id_thuoc
            """)
            medicines = cursor.fetchall()
            if not medicines:
                messagebox.showinfo("Thông báo", "Không có thuốc nào trong danh sách!")
            return medicines
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách thuốc: {e}")
            return []
        finally:
            cursor.close()

    def validate_prescription_data(self, prescription_data):
        """Kiểm tra dữ liệu kê đơn"""
        if not prescription_data["ID Lịch hẹn"]:
            messagebox.showerror("Lỗi", "Vui lòng chọn lịch hẹn!")
            return False
        if not prescription_data["Tên thuốc"]:
            messagebox.showerror("Lỗi", "Vui lòng chọn thuốc!")
            return False
        if not prescription_data["Số lượng"]:
            messagebox.showerror("Lỗi", "Số lượng thuốc không được để trống!")
            return False
        try:
            quantity = int(prescription_data["Số lượng"])
            if quantity <= 0:
                messagebox.showerror("Lỗi", "Số lượng thuốc phải lớn hơn 0!")
                return False
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng thuốc phải là số nguyên!")
            return False
        return True

    def prescribe_medicine(self, prescription_data):
        """Kê đơn và trừ số lượng thuốc trong kho"""
        if not self.connection:
            return False
        if not self.validate_prescription_data(prescription_data):
            return False

        id_lich_hen = int(prescription_data["ID Lịch hẹn"])
        ten_thuoc = prescription_data["Tên thuốc"].split(" (Số lượng:")[0].strip()
        quantity = int(prescription_data["Số lượng"])
        duration = prescription_data["Thời gian sử dụng"]
        huong_dan = prescription_data["Hướng dẫn"]
        danh_sach_thuoc = f"{ten_thuoc}, {quantity} viên, {duration}"

        cursor = self.connection.cursor()
        try:
            self.connection.start_transaction()

            cursor.execute("SELECT id FROM ke_don WHERE id_lich_hen = %s", (id_lich_hen,))
            if cursor.fetchone():
                messagebox.showerror("Lỗi", "Lịch hẹn này đã được kê đơn!")
                self.connection.rollback()
                return False

            cursor.execute("SELECT id_thu_cung, id_bac_si, ngay_hen, gio_hen FROM lich_hen WHERE id = %s", (id_lich_hen,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", "Lịch hẹn không tồn tại!")
                self.connection.rollback()
                return False
            id_thu_cung, id_bac_si, ngay_hen, gio_hen = result

            cursor.execute("""
                SELECT id FROM lich_hen
                WHERE id_thu_cung = %s AND ngay_hen = %s AND gio_hen = %s AND id != %s
            """, (id_thu_cung, ngay_hen, gio_hen, id_lich_hen))
            if cursor.fetchone():
                messagebox.showerror("Lỗi", "Vật nuôi này đã có lịch hẹn vào thời gian này!")
                self.connection.rollback()
                return False

            cursor.execute("SELECT id FROM thuoc WHERE ten_thuoc = %s", (ten_thuoc,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", f"Thuốc '{ten_thuoc}' không tồn tại!")
                self.connection.rollback()
                return False
            id_thuoc = result[0]

            cursor.execute("SELECT so_luong, han_su_dung FROM kho_thuoc WHERE id_thuoc = %s", (id_thuoc,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", f"Thuốc '{ten_thuoc}' không tồn tại trong kho!")
                self.connection.rollback()
                return False

            current_quantity, han_su_dung = result
            if han_su_dung < datetime.now().date():
                messagebox.showerror("Lỗi", "Thuốc đã hết hạn sử dụng!")
                self.connection.rollback()
                return False
            if current_quantity < quantity:
                messagebox.showerror("Lỗi", f"Số lượng trong kho không đủ! Hiện có: {current_quantity}")
                self.connection.rollback()
                return False

            new_quantity = current_quantity - quantity
            cursor.execute("UPDATE kho_thuoc SET so_luong = %s WHERE id_thuoc = %s", (new_quantity, id_thuoc))

            cursor.execute("""
                INSERT INTO ke_don (id_lich_hen, id_thu_cung, id_bac_si, danh_sach_thuoc, huong_dan, ngay_ke_don)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (id_lich_hen, id_thu_cung, id_bac_si, danh_sach_thuoc, huong_dan, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            self.connection.commit()
            messagebox.showinfo("Thành công", f"Đã kê đơn thành công. Số lượng còn lại: {new_quantity}")
            return True
        except mysql.connector.Error as e:
            self.connection.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi kê đơn: {e}")
            return False
        finally:
            cursor.close()

    def update_prescription(self, prescription_id, prescription_data):
        """Cập nhật đơn thuốc"""
        if not self.connection or not prescription_id:
            messagebox.showwarning("Cảnh báo", "Không thể kết nối CSDL hoặc chưa chọn đơn thuốc!")
            return False

        if not self.validate_prescription_data(prescription_data):
            return False

        id_lich_hen = int(prescription_data["ID Lịch hẹn"])
        ten_thuoc = prescription_data["Tên thuốc"].split(" (Số lượng:")[0].strip()
        quantity = int(prescription_data["Số lượng"])
        duration = prescription_data["Thời gian sử dụng"]
        huong_dan = prescription_data["Hướng dẫn"]
        danh_sach_thuoc = f"{ten_thuoc}, {quantity} viên, {duration}"

        cursor = self.connection.cursor()
        try:
            self.connection.start_transaction()

            cursor.execute("SELECT id FROM ke_don WHERE id_lich_hen = %s AND id != %s", (id_lich_hen, prescription_id))
            if cursor.fetchone():
                messagebox.showerror("Lỗi", "Lịch hẹn này đã được kê đơn!")
                self.connection.rollback()
                return False

            cursor.execute("SELECT id_thu_cung, ngay_hen, gio_hen FROM lich_hen WHERE id = %s", (id_lich_hen,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", "Lịch hẹn không tồn tại!")
                self.connection.rollback()
                return False
            id_thu_cung, ngay_hen, gio_hen = result

            cursor.execute("""
                SELECT id FROM lich_hen
                WHERE id_thu_cung = %s AND ngay_hen = %s AND gio_hen = %s AND id != %s
            """, (id_thu_cung, ngay_hen, gio_hen, id_lich_hen))
            if cursor.fetchone():
                messagebox.showerror("Lỗi", "Vật nuôi này đã có lịch hẹn vào thời gian này!")
                self.connection.rollback()
                return False

            cursor.execute("SELECT danh_sach_thuoc FROM ke_don WHERE id = %s", (prescription_id,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", "Đơn thuốc không tồn tại!")
                self.connection.rollback()
                return False

            parts = result[0].split(",")
            old_ten_thuoc = parts[0].strip() if parts else ""
            quantity_part = parts[1].strip() if len(parts) > 1 else "1"
            match = re.search(r'\d+', quantity_part)
            old_quantity = int(match.group()) if match else 1

            cursor.execute("SELECT id FROM thuoc WHERE ten_thuoc = %s", (old_ten_thuoc,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", f"Thuốc '{old_ten_thuoc}' không tồn tại!")
                self.connection.rollback()
                return False
            old_id_thuoc = result[0]

            cursor.execute("SELECT so_luong FROM kho_thuoc WHERE id_thuoc = %s", (old_id_thuoc,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", f"Thuốc '{old_ten_thuoc}' không tồn tại trong kho!")
                self.connection.rollback()
                return False
            current_quantity = result[0]
            cursor.execute("UPDATE kho_thuoc SET so_luong = %s WHERE id_thuoc = %s", (current_quantity + old_quantity, old_id_thuoc))

            cursor.execute("SELECT id FROM thuoc WHERE ten_thuoc = %s", (ten_thuoc,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", f"Thuốc '{ten_thuoc}' không tồn tại!")
                self.connection.rollback()
                return False
            id_thuoc = result[0]

            cursor.execute("SELECT so_luong, han_su_dung FROM kho_thuoc WHERE id_thuoc = %s", (id_thuoc,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", f"Thuốc '{ten_thuoc}' không tồn tại trong kho!")
                self.connection.rollback()
                return False

            current_quantity, han_su_dung = result
            if han_su_dung < datetime.now().date():
                messagebox.showerror("Lỗi", "Thuốc đã hết hạn sử dụng!")
                self.connection.rollback()
                return False
            if current_quantity < quantity:
                messagebox.showerror("Lỗi", f"Số lượng trong kho không đủ! Hiện có: {current_quantity}")
                self.connection.rollback()
                return False

            new_quantity = current_quantity - quantity
            cursor.execute("UPDATE kho_thuoc SET so_luong = %s WHERE id_thuoc = %s", (new_quantity, id_thuoc))

            cursor.execute("SELECT id_thu_cung, id_bac_si FROM lich_hen WHERE id = %s", (id_lich_hen,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", "Lịch hẹn không tồn tại!")
                self.connection.rollback()
                return False
            id_thu_cung, id_bac_si = result

            cursor.execute("""
                UPDATE ke_don
                SET id_lich_hen = %s, id_thu_cung = %s, id_bac_si = %s, danh_sach_thuoc = %s, huong_dan = %s, ngay_ke_don = %s
                WHERE id = %s
            """, (id_lich_hen, id_thu_cung, id_bac_si, danh_sach_thuoc, huong_dan, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), prescription_id))

            self.connection.commit()
            messagebox.showinfo("Thành công", "Cập nhật đơn thuốc thành công!")
            return True
        except mysql.connector.Error as e:
            self.connection.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật đơn thuốc: {e}")
            return False
        finally:
            cursor.close()

    def delete_prescription(self, prescription_id):
        """Xóa đơn thuốc và hoàn trả số lượng thuốc vào kho"""
        if not self.connection or not prescription_id:
            messagebox.showwarning("Cảnh báo", "Không thể kết nối CSDL hoặc chưa chọn đơn thuốc!")
            return False

        cursor = self.connection.cursor()
        try:
            self.connection.start_transaction()

            cursor.execute("SELECT danh_sach_thuoc FROM ke_don WHERE id = %s", (prescription_id,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", "Đơn thuốc không tồn tại!")
                self.connection.rollback()
                return False

            parts = result[0].split(",")
            ten_thuoc = parts[0].strip() if parts else ""
            quantity_part = parts[1].strip() if len(parts) > 1 else "1"
            match = re.search(r'\d+', quantity_part)
            quantity = int(match.group()) if match else 1

            cursor.execute("SELECT id FROM thuoc WHERE ten_thuoc = %s", (ten_thuoc,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", f"Thuốc '{ten_thuoc}' không tồn tại!")
                self.connection.rollback()
                return False
            id_thuoc = result[0]

            cursor.execute("SELECT so_luong FROM kho_thuoc WHERE id_thuoc = %s", (id_thuoc,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("Lỗi", f"Thuốc '{ten_thuoc}' không tồn tại trong kho!")
                self.connection.rollback()
                return False

            current_quantity = result[0]
            cursor.execute("UPDATE kho_thuoc SET so_luong = %s WHERE id_thuoc = %s", (current_quantity + quantity, id_thuoc))

            cursor.execute("DELETE FROM ke_don WHERE id = %s", (prescription_id,))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Xóa đơn thuốc thành công!")
            return True
        except mysql.connector.Error as e:
            self.connection.rollback()
            messagebox.showerror("Lỗi", f"Lỗi khi xóa đơn thuốc: {e}")
            return False
        finally:
            cursor.close()

    def search_prescriptions(self, keyword, field):
        """Tìm kiếm đơn thuốc"""
        if not self.connection:
            return []
        if not keyword or not field:
            return self.get_all_prescriptions()

        keyword = keyword.strip()
        cursor = self.connection.cursor()
        sql = """
        SELECT ke_don.id, ke_don.id_lich_hen, thu_cung.ten, bac_si.ho_ten, 
               ke_don.danh_sach_thuoc, ke_don.huong_dan, ke_don.ngay_ke_don
        FROM ke_don
        JOIN thu_cung ON ke_don.id_thu_cung = thu_cung.id
        JOIN bac_si ON ke_don.id_bac_si = bac_si.id
        WHERE LOWER(ke_don.id) LIKE LOWER(%s)
           OR LOWER(ke_don.id_lich_hen) LIKE LOWER(%s)
           OR LOWER(thu_cung.ten) LIKE LOWER(%s)
           OR LOWER(bac_si.ho_ten) LIKE LOWER(%s)
           OR LOWER(ke_don.danh_sach_thuoc) LIKE LOWER(%s)
           OR LOWER(ke_don.huong_dan) LIKE LOWER(%s)
           OR LOWER(ke_don.ngay_ke_don) LIKE LOWER(%s)
        """
        try:
            keyword_pattern = f'%{keyword}%'
            cursor.execute(sql, (keyword_pattern,) * 7)
            return cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm đơn thuốc: {e}")
            return []
        finally:
            cursor.close()

    def get_all_prescriptions(self):
        """Lấy danh sách tất cả đơn thuốc"""
        if not self.connection:
            return []
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                SELECT ke_don.id, ke_don.id_lich_hen, thu_cung.ten, bac_si.ho_ten, 
                       ke_don.danh_sach_thuoc, ke_don.huong_dan, ke_don.ngay_ke_don
                FROM ke_don
                JOIN thu_cung ON ke_don.id_thu_cung = thu_cung.id
                JOIN bac_si ON ke_don.id_bac_si = bac_si.id
            """)
            prescriptions = cursor.fetchall()
            if not prescriptions:
                messagebox.showinfo("Thông báo", "Không có đơn thuốc nào!")
            return prescriptions
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách đơn thuốc: {e}")
            return []
        finally:
            cursor.close()

    def __del__(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()