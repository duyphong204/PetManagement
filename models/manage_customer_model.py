import mysql.connector
import re
from tkinter import messagebox

class CustomerModel:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="qlthucung2"  # Change to a database for customers (qlkhachhang)
        )

    def validate_customer_data(self, customer_data):
       
        if not customer_data["Tên khách hàng"]:
            messagebox.showerror("Lỗi", "Tên khách hàng không được để trống!")
            return False
        if not customer_data["Số điện thoại"]:
            messagebox.showerror("Lỗi", "Số điện thoại không được để trống!")
            return False
        if not customer_data["Số điện thoại"].isdigit() or len(customer_data["Số điện thoại"]) != 10:
            messagebox.showerror("Lỗi", "Số điện thoại phải có đúng 10 chữ số!")
            return False
        if not customer_data["Số điện thoại"].startswith("0"):  # Kiểm tra bắt đầu bằng số 0
            messagebox.showerror("Lỗi", "Số điện thoại phải bắt đầu bằng số 0!")
            return False
        if not customer_data["Email"]:
            messagebox.showerror("Lỗi", "Email không được để trống!")
            return False
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.com$", customer_data["Email"]):
             messagebox.showerror("Lỗi", "Định dạng Email không đúng'!")
             return False
        if not customer_data["Địa chỉ"]:
            messagebox.showerror("Lỗi", "Địa chỉ không được để trống!")
            return False
        if not customer_data["ID người dùng"]:
            messagebox.showerror("Lỗi", "ID người dùng không được để trống!")
            return False
        return True
    

    def add_customer(self, customer_data):
        """Thêm một khách hàng mới vào bảng khách_hang."""
        if self.validate_customer_data(customer_data):
            cursor = self.connection.cursor()

            # Kiểm tra dữ liệu trước khi chạy SQL
           # print("Dữ liệu khách hàng:", customer_data)  


            sql = """
            INSERT INTO chu_so_huu (ho_ten, so_dien_thoai, email, dia_chi, id_nguoi_dung)
            VALUES (%s, %s, %s, %s, %s)
            """
           
            try:
                cursor.execute(sql, (
                    customer_data["Tên khách hàng"], customer_data["Số điện thoại"], 
                    customer_data["Email"], customer_data["Địa chỉ"], customer_data["ID người dùng"]
                ))
                self.connection.commit()
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm khách hàng: {e}")
            finally:
                cursor.close()

    def delete_customer(self, customer_id):
        """Xóa một khách hàng khỏi bảng khách_hang bằng ID."""
        if not customer_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để xóa!")
            return
        cursor = self.connection.cursor()
        sql = "DELETE FROM chu_so_huu WHERE id = %s"
        try:
            cursor.execute(sql, (customer_id,))
            self.connection.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa khách hàng: {e}")
        finally:
            cursor.close()

    def update_customer(self, customer_data):
        """Cập nhật thông tin của một khách hàng."""
        if self.validate_customer_data(customer_data):
            cursor = self.connection.cursor()
            sql = """
            UPDATE chu_so_huu
            SET ho_ten = %s, so_dien_thoai = %s, email = %s, dia_chi = %s, id_nguoi_dung = %s
            WHERE id = %s
            """
            try:
                cursor.execute(sql, (
                    customer_data["Tên khách hàng"], customer_data["Số điện thoại"], customer_data["Email"], customer_data["Địa chỉ"],
                    customer_data["ID người dùng"], customer_data["ID khách hàng"]
                ))
                self.connection.commit()
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi cập nhật khách hàng: {e}")
            finally:
                cursor.close()

    def search_customers(self, keyword, field):
        """Tìm kiếm khách hàng theo một trường cụ thể."""
        if not keyword or not field:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa và chọn trường tìm kiếm!")
            return []
        cursor = self.connection.cursor()
        sql = f"SELECT * FROM chu_so_huu WHERE {field} LIKE %s"
        try:
            cursor.execute(sql, ('%' + keyword + '%',))
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {e}")
            return []
        finally:
            cursor.close()

    def get_all_customers(self):
        """Lấy danh sách tất cả khách hàng trong hệ thống."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM chu_so_huu")
            customers = cursor.fetchall()
            if not customers:
                messagebox.showinfo("Thông báo", "Không có dữ liệu khách hàng trong CSDL!")
            return customers
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách: {e}")
            return []
        finally:
            cursor.close()

    def delete_all_customers(self):
        """Xóa tất cả khách hàng"""
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM chu_so_huu")
            self.connection.commit()
            messagebox.showinfo("Thành công", "Đã xóa tất cả khách hàng!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa tất cả: {e}")
        finally:
            cursor.close()

    def __del__(self):
        """Đóng kết nối khi đối tượng bị hủy."""
        if self.connection.is_connected():
            self.connection.close()