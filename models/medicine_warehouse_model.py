import mysql.connector
from tkinter import messagebox
from datetime import datetime

class MedicineWarehouseModel:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="qlthucung2"
        )

    def validate_medicine_data(self, medicine_data, check_duplicate=True):
        """Kiểm tra dữ liệu thuốc trước khi thêm hoặc sửa"""

        # Kiểm tra tên thuốc
        ten_thuoc = medicine_data.get("Tên thuốc", "").strip()
        if not ten_thuoc:
            messagebox.showerror("Lỗi", "Tên thuốc không được để trống!")
            return False

        # Kiểm tra số lượng
        so_luong = medicine_data.get("Số lượng", "")
        if not so_luong.isdigit() or int(so_luong) <= 0:
            messagebox.showerror("Lỗi", "Số lượng thuốc phải là số dương!")
            return False

        # Kiểm tra ngày nhập
        if not medicine_data["Ngày nhập"]:
            medicine_data["Ngày nhập"] = datetime.now().strftime('%Y-%m-%d')
        else:
            try:
                datetime.strptime(medicine_data["Ngày nhập"], '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Lỗi", "Ngày nhập không hợp lệ! (Định dạng: YYYY-MM-DD)")
                return False

        # Kiểm tra hạn sử dụng
        if not medicine_data["Hạn sử dụng"]:
            messagebox.showerror("Lỗi", "Hạn sử dụng không được để trống!")
            return False
        try:
            datetime.strptime(medicine_data["Hạn sử dụng"], '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Lỗi", "Hạn sử dụng không hợp lệ! (Định dạng: YYYY-MM-DD)")
            return False

        # Kiểm tra tên thuốc có bị trùng khi thêm mới
        if check_duplicate:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM kho_thuoc WHERE ten_thuoc = %s", (ten_thuoc,))
            if cursor.fetchone():
                messagebox.showerror("Lỗi", "Tên thuốc đã tồn tại trong kho!")
                cursor.close()
                return False
            cursor.close()

        return True

    def add_medicine(self, medicine_data):
        """Thêm thuốc mới vào bảng kho_thuoc"""
        if self.validate_medicine_data(medicine_data, check_duplicate=True):
            cursor = self.connection.cursor()
            try:
                # Thêm trực tiếp vào bảng kho_thuoc với ten_thuoc
                sql = """
                INSERT INTO kho_thuoc (ten_thuoc, so_luong, ngay_nhap, han_su_dung)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    medicine_data["Tên thuốc"],
                    medicine_data["Số lượng"],
                    medicine_data["Ngày nhập"],
                    medicine_data["Hạn sử dụng"]
                ))
                self.connection.commit()
                messagebox.showinfo("Thành công", "Thêm thuốc thành công!")
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm thuốc: {e}")
            finally:
                cursor.close()

    def delete_medicine(self, medicine_id):
        """Xóa thuốc khỏi kho"""
        if not medicine_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thuốc để xóa!")
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM kho_thuoc WHERE id = %s", (medicine_id,))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Xóa thuốc thành công!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa thuốc: {e}")
        finally:
            cursor.close()

    def update_medicine(self, medicine_data):
        """Cập nhật thuốc trong kho"""
        if self.validate_medicine_data(medicine_data, check_duplicate=False):
            cursor = self.connection.cursor()
            try:
                # Cập nhật trực tiếp trong bảng kho_thuoc
                sql = """
                UPDATE kho_thuoc
                SET ten_thuoc = %s, so_luong = %s, ngay_nhap = %s, han_su_dung = %s
                WHERE id = %s
                """
                cursor.execute(sql, (
                    medicine_data["Tên thuốc"],
                    medicine_data["Số lượng"],
                    medicine_data["Ngày nhập"],
                    medicine_data["Hạn sử dụng"],
                    medicine_data["ID"]
                ))
                self.connection.commit()
                messagebox.showinfo("Thành công", "Cập nhật thuốc thành công!")
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi cập nhật thuốc: {e}")
            finally:
                cursor.close()

    def search_medicines(self, keyword, field):
        """Tìm kiếm thuốc"""
        if not keyword or not field:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa và chọn trường tìm kiếm!")
            return []
        cursor = self.connection.cursor()
        field_mapping = {
            "Tên thuốc": "ten_thuoc",
            "Số lượng": "so_luong",
            "Ngày nhập": "ngay_nhap",
            "Hạn sử dụng": "han_su_dung"
        }
        db_field = field_mapping.get(field, "ten_thuoc")
        sql = f"""
        SELECT id, ten_thuoc, so_luong, ngay_nhap, han_su_dung
        FROM kho_thuoc
        WHERE {db_field} LIKE %s
        """
        try:
            cursor.execute(sql, ('%' + keyword + '%',))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm thuốc: {e}")
            return []
        finally:
            cursor.close()

    def get_all_medicines(self):
        """Lấy tất cả thuốc trong kho"""
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            SELECT id, ten_thuoc, so_luong, ngay_nhap, han_su_dung
            FROM kho_thuoc
            """)
            results = cursor.fetchall()
            if not results:
                messagebox.showinfo("Thông báo", "Không có thuốc nào trong kho!")
            return results
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách thuốc: {e}")
            return []
        finally:
            cursor.close()

    def delete_all_medicines(self):
        """Xóa toàn bộ thuốc trong kho"""
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM kho_thuoc")
            self.connection.commit()
            messagebox.showinfo("Thành công", "Đã xóa toàn bộ kho thuốc!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa toàn bộ thuốc: {e}")
        finally:
            cursor.close()

    def __del__(self):
        """Đóng kết nối"""
        if self.connection.is_connected():
            self.connection.close()