import mysql.connector
from tkinter import messagebox

class TreatmentModel:
    def __init__(self):
        """
        Khởi tạo kết nối cơ sở dữ liệu.
        """
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="qlthucung"
            )
            print("Kết nối cơ sở dữ liệu thành công!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến cơ sở dữ liệu: {e}")

    def validate_treatment_data(self, treatment_data):
        """
        Xác thực dữ liệu điều trị trước khi thực hiện các thao tác.
        """
        if not treatment_data.get("id_lich_hen"):
            messagebox.showwarning("Cảnh báo", "ID lịch hẹn không được để trống!")
            return False
        if not treatment_data.get("id_thu_cung"):
            messagebox.showwarning("Cảnh báo", "ID thú cưng không được để trống!")
            return False
        if not treatment_data.get("id_bac_si"):
            messagebox.showwarning("Cảnh báo", "ID bác sĩ không được để trống!")
            return False
        if not treatment_data.get("ngay_dieu_tri"):
            messagebox.showwarning("Cảnh báo", "Ngày điều trị không được để trống!")
            return False
        if not treatment_data.get("chan_doan"):
            messagebox.showwarning("Cảnh báo", "Chẩn đoán không được để trống!")
            return False
        if not treatment_data.get("chi_phi"):
            messagebox.showwarning("Cảnh báo", "Chi phí không được để trống!")
            return False
        return True

    def add_treatment(self, treatment_data):
        """
        Thêm một điều trị mới vào cơ sở dữ liệu.
        """
        if not self.validate_treatment_data(treatment_data):
            return
        cursor = self.connection.cursor()
        sql = """
        INSERT INTO dieu_tri (id_lich_hen, id_thu_cung, id_bac_si, ngay_dieu_tri, chan_doan, don_thuoc, chi_phi)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (
                treatment_data["id_lich_hen"], treatment_data["id_thu_cung"], treatment_data["id_bac_si"],
                treatment_data["ngay_dieu_tri"], treatment_data["chan_doan"], treatment_data.get("don_thuoc", ""),
                treatment_data["chi_phi"]
            ))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Thêm điều trị thành công!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm điều trị: {e}")
        finally:
            cursor.close()

    def delete_treatment(self, id):
        """
        Xóa một điều trị khỏi cơ sở dữ liệu.
        """
        if not id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn điều trị để xóa!")
            return
        cursor = self.connection.cursor()
        sql = "DELETE FROM dieu_tri WHERE id = %s"
        try:
            cursor.execute(sql, (id,))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Xóa điều trị thành công!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa điều trị: {e}")
        finally:
            cursor.close()

    def update_treatment(self, treatment_data):
        """
        Cập nhật thông tin điều trị trong cơ sở dữ liệu.
        """
        if not self.validate_treatment_data(treatment_data):
            return
        cursor = self.connection.cursor()
        sql = """
        UPDATE dieu_tri
        SET id_lich_hen = %s, id_thu_cung = %s, id_bac_si = %s, ngay_dieu_tri = %s,
            chan_doan = %s, don_thuoc = %s, chi_phi = %s
        WHERE id = %s
        """
        try:
            cursor.execute(sql, (
                treatment_data["id_lich_hen"], treatment_data["id_thu_cung"], treatment_data["id_bac_si"],
                treatment_data["ngay_dieu_tri"], treatment_data["chan_doan"], treatment_data.get("don_thuoc", ""),
                treatment_data["chi_phi"], treatment_data["id"]
            ))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Cập nhật điều trị thành công!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật điều trị: {e}")
        finally:
            cursor.close()

    def get_all_treatments(self):
        """
        Lấy danh sách tất cả các điều trị từ cơ sở dữ liệu.
        """
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM dieu_tri")
            treatments = cursor.fetchall()
            if not treatments:
                messagebox.showinfo("Thông báo", "Không có dữ liệu điều trị trong CSDL!")
            return treatments
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách: {e}")
            return []
        finally:
            cursor.close()

    def search_treatments(self, conditions):
        """
        Tìm kiếm điều trị dựa trên các điều kiện.
        """
        if not conditions:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ít nhất một điều kiện tìm kiếm!")
            return []

        cursor = self.connection.cursor(dictionary=True)
        sql = """
        SELECT id, id_lich_hen, id_thu_cung, id_bac_si, ngay_dieu_tri, chan_doan, don_thuoc, chi_phi
        FROM dieu_tri
        WHERE 1=1
        """
        params = []

        if "ngay_dieu_tri >=" in conditions and conditions["ngay_dieu_tri >="]:
            sql += " AND ngay_dieu_tri >= %s"
            params.append(conditions["ngay_dieu_tri >="])
        if "ngay_dieu_tri <=" in conditions and conditions["ngay_dieu_tri <="]:
            sql += " AND ngay_dieu_tri <= %s"
            params.append(conditions["ngay_dieu_tri <="])
        if "keyword" in conditions and conditions["keyword"]:
            keyword = f"%{conditions['keyword']}%"
            sql += """
            AND (
                CAST(id AS CHAR) LIKE %s OR
                CAST(id_lich_hen AS CHAR) LIKE %s OR
                CAST(id_thu_cung AS CHAR) LIKE %s OR
                CAST(id_bac_si AS CHAR) LIKE %s OR
                chan_doan LIKE %s OR
                don_thuoc LIKE %s
            )
            """
            params.extend([keyword, keyword, keyword, keyword, keyword, keyword])

        try:
            cursor.execute(sql, tuple(params))
            results = cursor.fetchall()
            if not results:
                messagebox.showinfo("Thông báo", "Không tìm thấy kết quả phù hợp!")
            return results
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {e}")
            return []
        finally:
            cursor.close()

    def __del__(self):
        """
        Đóng kết nối cơ sở dữ liệu khi đối tượng bị hủy.
        """
        if self.connection.is_connected():
            self.connection.close()
