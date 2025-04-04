import mysql.connector
from tkinter import messagebox
import re
from datetime import datetime

class MedicineWarehouseModel:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="qlthucung"  # Cập nhật thành database phù hợp với quản lý kho thuốc
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
        messagebox.showerror("Lỗi", "Ngày nhập không được để trống!")
        return False
     try:
        # Kiểm tra định dạng ngày nhập
        datetime.strptime(medicine_data["Ngày nhập"], '%Y-%m-%d')
     except ValueError:
        messagebox.showerror("Lỗi", "Ngày nhập không hợp lệ! (Định dạng: YYYY-MM-DD)")
        return False
     
    
     # Kiểm tra ngày xuất (Định dạng: YYYY-MM-DD)
     if not medicine_data["Ngày xuất"]:
        messagebox.showerror("Lỗi", "Ngày xuất không được để trống!")
        return False
     elif medicine_data["Ngày xuất"] == "0":
        # Nếu nhập "0", gán "None"
        medicine_data["Ngày xuất"] = "None"
     else:
        try:
            # Kiểm tra định dạng ngày xuất nếu có nhập
            datetime.strptime(medicine_data["Ngày xuất"], '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Lỗi", "Ngày xuất không hợp lệ! (Định dạng: YYYY-MM-DD)")
            return False


    # Nếu tất cả các trường hợp trên không lỗi, trả về True
     return True


    def add_medicine(self, medicine_data):
        """Thêm một loại thuốc mới vào kho."""
        if self.validate_medicine_data(medicine_data):
            cursor = self.connection.cursor()
            sql = """
            INSERT INTO kho_thuoc (ten_thuoc, so_luong, ngay_nhap, ngay_xuat, ghi_chu)
            VALUES (%s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(sql, (
                    medicine_data["Tên thuốc"], medicine_data["Số lượng"], 
                    medicine_data["Ngày nhập"], medicine_data["Ngày xuất"], medicine_data["Ghi chú"]
                ))
                self.connection.commit()
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
        sql = "DELETE FROM kho_thuoc WHERE id_khothuoc = %s"
        try:
            cursor.execute(sql, (medicine_id,))
            self.connection.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa thuốc: {e}")
        finally:
            cursor.close()

    def update_medicine(self, medicine_data):
        """Cập nhật thông tin thuốc trong kho."""
        if self.validate_medicine_data(medicine_data):
            cursor = self.connection.cursor()
            sql = """
            UPDATE kho_thuoc
            SET ten_thuoc = %s, so_luong = %s, ngay_nhap = %s, ngay_xuat = %s, ghi_chu = %s
            WHERE id_khothuoc = %s
            """
            try:
                cursor.execute(sql, (
                    medicine_data["Tên thuốc"], medicine_data["Số lượng"], 
                    medicine_data["Ngày nhập"], medicine_data["Ngày xuất"], 
                    medicine_data["Ghi chú"], medicine_data["ID kho thuốc"]
                ))
                self.connection.commit()
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
        sql = f"SELECT * FROM kho_thuoc WHERE {field} LIKE %s"
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
            cursor.execute("SELECT * FROM kho_thuoc")
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
