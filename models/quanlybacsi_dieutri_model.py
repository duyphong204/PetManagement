import mysql.connector
import re
from tkinter import messagebox

class TreatmentModel:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Thay bằng mật khẩu của bạn nếu có
                database="qlthucung2"
            )
            print("Kết nối CSDL thành công!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối CSDL: {e}")
            self.connection = None
    def validate_date(self, date):
        """ Kiểm tra định dạng ngày (yyyy-mm-dd) """
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        return bool(re.match(pattern, date))

    def add_treatment(self, treatment_data):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return False

        # Kiểm tra ngày
        if not self.validate_date(treatment_data["Ngày điều trị"]):
            messagebox.showerror("Lỗi", "Ngày điều trị phải theo định dạng yyyy-mm-dd")
            return False

        cursor = self.connection.cursor()

        # Kiểm tra xem id_thu_cung và id_bac_si có tồn tại trong bảng thu_cung và bac_si không
        cursor.execute("SELECT COUNT(*) FROM thu_cung WHERE id = %s", (treatment_data["ID Thú cưng"],))
        if cursor.fetchone()[0] == 0:
            messagebox.showerror("Lỗi", "ID Thú cưng không tồn tại trong cơ sở dữ liệu")
            return False

        cursor.execute("SELECT COUNT(*) FROM bac_si WHERE id = %s", (treatment_data["ID Bác sĩ"],))
        if cursor.fetchone()[0] == 0:
            messagebox.showerror("Lỗi", "ID Bác sĩ không tồn tại trong cơ sở dữ liệu")
            return False

        sql = """
        INSERT INTO dieu_tri (id_thu_cung, id_bac_si, ngay_dieu_tri, chan_doan, ke_don_thuoc, lieu_luong, ghi_chu, chi_phi)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (
                treatment_data["ID Thú cưng"], treatment_data["ID Bác sĩ"],
                treatment_data["Ngày điều trị"], treatment_data["Chẩn đoán"],
                treatment_data["Kê đơn thuốc"], treatment_data["Liều lượng"],
                treatment_data["Ghi chú"], treatment_data["Chi phí"]
            ))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm điều trị: {e}")
            return False
        finally:
            cursor.close()


    def delete_treatment(self, treatment_id):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return False
        cursor = self.connection.cursor()
        sql = "DELETE FROM dieu_tri WHERE id = %s"
        try:
            cursor.execute(sql, (treatment_id,))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa điều trị: {e}")
            return False
        finally:
            cursor.close()

    def update_treatment(self, treatment_id, treatment_data):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return False

        # Kiểm tra ngày
        if not self.validate_date(treatment_data["Ngày điều trị"]):
            messagebox.showerror("Lỗi", "Ngày điều trị phải theo định dạng yyyy-mm-dd!")
            return False

        cursor = self.connection.cursor()

        # Kiểm tra xem id_thu_cung và id_bac_si có tồn tại trong bảng thu_cung và bac_si không
        cursor.execute("SELECT COUNT(*) FROM thu_cung WHERE id = %s", (treatment_data["ID Thú cưng"],))
        if cursor.fetchone()[0] == 0:
            messagebox.showerror("Lỗi", "ID Thú cưng không tồn tại trong cơ sở dữ liệu!")
            return False

        cursor.execute("SELECT COUNT(*) FROM bac_si WHERE id = %s", (treatment_data["ID Bác sĩ"],))
        if cursor.fetchone()[0] == 0:
            messagebox.showerror("Lỗi", "ID Bác sĩ không tồn tại trong cơ sở dữ liệu!")
            return False

        sql = """
        UPDATE dieu_tri
        SET id_thu_cung = %s, id_bac_si = %s, ngay_dieu_tri = %s, chan_doan = %s, ke_don_thuoc = %s, 
        lieu_luong = %s, ghi_chu = %s, chi_phi = %s
        WHERE id = %s
        """
        try:
            cursor.execute(sql, (
                treatment_data["ID Thú cưng"], treatment_data["ID Bác sĩ"],
                treatment_data["Ngày điều trị"], treatment_data["Chẩn đoán"],
                treatment_data["Kê đơn thuốc"], treatment_data["Liều lượng"],
                treatment_data["Ghi chú"], treatment_data["Chi phí"], treatment_id
            ))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật điều trị: {e}")
            return False
        finally:
            cursor.close()

    def search_treatments(self, keyword):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return []
        cursor = self.connection.cursor()
        sql = """
        SELECT id, id_thu_cung, id_bac_si, ngay_dieu_tri, chan_doan, ke_don_thuoc, lieu_luong, ghi_chu, chi_phi
        FROM dieu_tri 
        WHERE id_thu_cung LIKE %s OR chan_doan LIKE %s OR id_bac_si LIKE %s
        """
        try:
            search_pattern = f"%{keyword}%"
            cursor.execute(sql, (search_pattern, search_pattern, search_pattern))
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm điều trị: {e}")
            return []
        finally:
            cursor.close()

    def get_all_treatments(self):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return []
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, id_thu_cung, id_bac_si, ngay_dieu_tri, chan_doan, ke_don_thuoc, lieu_luong, ghi_chu, chi_phi FROM dieu_tri")
            treatments = cursor.fetchall()
            return treatments
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách điều trị: {e}")
            return []
        finally:
            cursor.close()

    def get_next_available_id(self):
        """ Tìm ID nhỏ nhất chưa được sử dụng trong bảng dieu_tri """
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM dieu_tri ORDER BY id ASC")
        used_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()

        if not used_ids or used_ids[0] != 1:
            return 1  

        for i in range(1, len(used_ids) + 2): 
            if i not in used_ids:
                return i