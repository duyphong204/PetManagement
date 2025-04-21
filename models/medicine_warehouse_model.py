import mysql.connector
from tkinter import messagebox
from datetime import datetime

class MedicineWarehouseModel:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="qlthucung2"  # Đổi sang qlthucung2
        )

    def validate_medicine_data(self, medicine_data):
        """Kiểm tra dữ liệu thuốc trước khi thêm hoặc sửa"""
        # Kiểm tra tên thuốc
        if not medicine_data["Tên thuốc"]:
            messagebox.showerror("Lỗi", "Tên thuốc không được để trống!")
            return False

        # Kiểm tra số lượng
        if not medicine_data["Số lượng"].isdigit() or int(medicine_data["Số lượng"]) <= 0:
            messagebox.showerror("Lỗi", "Số lượng thuốc phải là số dương!")
            return False

        # Kiểm tra ngày nhập (Định dạng: YYYY-MM-DD)
        if not medicine_data["Ngày nhập"]:
            medicine_data["Ngày nhập"] = datetime.now().strftime('%Y-%m-%d')
        else:
            try:
                datetime.strptime(medicine_data["Ngày nhập"], '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Lỗi", "Ngày nhập không hợp lệ! (Định dạng: YYYY-MM-DD)")
                return False

        # Kiểm tra hạn sử dụng (Định dạng: YYYY-MM-DD)
        if not medicine_data["Hạn sử dụng"]:
            messagebox.showerror("Lỗi", "Hạn sử dụng không được để trống!")
            return False
        try:
            datetime.strptime(medicine_data["Hạn sử dụng"], '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Lỗi", "Hạn sử dụng không hợp lệ! (Định dạng: YYYY-MM-DD)")
            return False

        # Kiểm tra xem tên thuốc có tồn tại trong bảng thuoc không
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM thuoc WHERE ten_thuoc = %s", (medicine_data["Tên thuốc"],))
        if not cursor.fetchone():
            messagebox.showerror("Lỗi", "Tên thuốc không tồn tại trong danh sách thuốc!")
            cursor.close()
            return False
        cursor.close()

        return True

    def add_medicine(self, medicine_data):
        """Thêm một loại thuốc mới vào kho."""
        if self.validate_medicine_data(medicine_data):
            cursor = self.connection.cursor()
            # Lấy id_thuoc từ ten_thuoc
            cursor.execute("SELECT id FROM thuoc WHERE ten_thuoc = %s", (medicine_data["Tên thuốc"],))
            id_thuoc = cursor.fetchone()[0]

            sql = """
            INSERT INTO kho_thuoc (id_thuoc, so_luong, ngay_nhap, han_su_dung)
            VALUES (%s, %s, %s, %s)
            """
            try:
                cursor.execute(sql, (
                    id_thuoc, medicine_data["Số lượng"],
                    medicine_data["Ngày nhập"], medicine_data["Hạn sử dụng"]
                ))
                self.connection.commit()
                messagebox.showinfo("Thành công", "Thêm thuốc thành công!")
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm thuốc: {e}")
            finally:
                cursor.close()

    def delete_medicine(self, medicine_id):
        """Xóa một loại thuốc khỏi kho bằng ID."""
        if not medicine_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thuốc để xóa!")
            return
        cursor = self.connection.cursor()
        sql = "DELETE FROM kho_thuoc WHERE id = %s"
        try:
            cursor.execute(sql, (medicine_id,))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Xóa thuốc thành công!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa thuốc: {e}")
        finally:
            cursor.close()

    def update_medicine(self, medicine_data):
        """Cập nhật thông tin thuốc trong kho."""
        if self.validate_medicine_data(medicine_data):
            cursor = self.connection.cursor()
            # Lấy id_thuoc từ ten_thuoc
            cursor.execute("SELECT id FROM thuoc WHERE ten_thuoc = %s", (medicine_data["Tên thuốc"],))
            id_thuoc = cursor.fetchone()[0]

            sql = """
            UPDATE kho_thuoc
            SET id_thuoc = %s, so_luong = %s, ngay_nhap = %s, han_su_dung = %s
            WHERE id = %s
            """
            try:
                cursor.execute(sql, (
                    id_thuoc, medicine_data["Số lượng"],
                    medicine_data["Ngày nhập"], medicine_data["Hạn sử dụng"],
                    medicine_data["ID"]
                ))
                self.connection.commit()
                messagebox.showinfo("Thành công", "Cập nhật thuốc thành công!")
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi cập nhật thuốc: {e}")
            finally:
                cursor.close()

    def search_medicines(self, keyword, field):
        """Tìm kiếm thuốc theo một tiêu chí cụ thể."""
        if not keyword or not field:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa và chọn trường tìm kiếm!")
            return []
        cursor = self.connection.cursor()
        field_mapping = {
            "Tên thuốc": "thuoc.ten_thuoc",
            "Số lượng": "kho_thuoc.so_luong",
            "Ngày nhập": "kho_thuoc.ngay_nhap",
            "Hạn sử dụng": "kho_thuoc.han_su_dung"
        }
        db_field = field_mapping.get(field, "thuoc.ten_thuoc")
        sql = f"""
        SELECT kho_thuoc.id, thuoc.ten_thuoc, kho_thuoc.so_luong, kho_thuoc.ngay_nhap, kho_thuoc.han_su_dung
        FROM kho_thuoc
        JOIN thuoc ON kho_thuoc.id_thuoc = thuoc.id
        WHERE {db_field} LIKE %s
        """
        try:
            cursor.execute(sql, ('%' + keyword + '%',))
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm thuốc: {e}")
            return []
        finally:
            cursor.close()

    def get_all_medicines(self):
        """Lấy danh sách tất cả thuốc trong kho."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
            SELECT kho_thuoc.id, thuoc.ten_thuoc, kho_thuoc.so_luong, kho_thuoc.ngay_nhap, kho_thuoc.han_su_dung
            FROM kho_thuoc
            JOIN thuoc ON kho_thuoc.id_thuoc = thuoc.id
            """)
            medicines = cursor.fetchall()
            if not medicines:
                messagebox.showinfo("Thông báo", "Không có thuốc nào trong kho!")
            return medicines
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách thuốc: {e}")
            return []
        finally:
            cursor.close()

    def delete_all_medicines(self):
        """Xóa toàn bộ thuốc trong kho."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM kho_thuoc")
            self.connection.commit()
            messagebox.showinfo("Thành công", "Đã xóa toàn bộ kho thuốc!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa tất cả thuốc: {e}")
        finally:
            cursor.close()

    def __del__(self):
        """Đóng kết nối khi đối tượng bị hủy."""
        if self.connection.is_connected():
            self.connection.close()