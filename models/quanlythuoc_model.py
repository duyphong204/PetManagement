import mysql.connector
import re
from tkinter import messagebox

class DrugModel:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Thay bằng mật khẩu của bạn nếu có
                database="qlthucung1"
            )
            print("Kết nối CSDL thành công!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối CSDL: {e}")
            self.connection = None

    def validate_medicine_data(self, medicine_data):
        """ Kiểm tra dữ liệu đầu vào của thuốc """
        
        # Kiểm tra tên thuốc không được để trống
        if not medicine_data["Tên thuốc"]:
            messagebox.showerror("Lỗi", "Tên thuốc không được để trống")
            return False
        
        # Kiểm tra đơn vị thuốc hợp lệ
        valid_units = ["Viên", "Chai", "Gói", "Ống"]
        if medicine_data["Đơn vị"] not in valid_units:
            messagebox.showerror("Lỗi", f"Đơn vị thuốc phải là một trong các giá trị: {', '.join(valid_units)}")
            return False
        
        # Kiểm tra giá trị gia không âm
        try:
            gia = float(medicine_data["Giá"])
            if gia < 0:
                messagebox.showerror("Lỗi", "Giá không được nhỏ hơn 0")
                return False
        except ValueError:
            messagebox.showerror("Lỗi", "Giá phải là một số hợp lệ")
            return False
        
        # Kiểm tra hạn sử dụng
        if not medicine_data["Hạn sử dụng"]:
            messagebox.showerror("Lỗi", "Hạn sử dụng không được để trống")
            return False
        
        
        try:
            so_luong = int(medicine_data["Số lượng"])
            if so_luong < 0:
                messagebox.showerror("Lỗi", "Số lượng không được nhỏ hơn 0")
                return False
        except ValueError:
            messagebox.showerror("Lỗi", "Số lượng phải là số nguyên hợp lệ")
            return False

        return True

    def get_next_available_id(self):
        """ Tìm ID nhỏ nhất chưa được sử dụng trong bảng thuốc """
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM thuoc ORDER BY id ASC")
        used_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()

        if not used_ids or used_ids[0] != 1:
            return 1  # Nếu bảng rỗng hoặc ID bắt đầu từ 1 bị thiếu, trả về 1

        for i in range(1, len(used_ids) + 2):  # +2 để xét cả trường hợp cuối
            if i not in used_ids:
                return i

    def add_medicine(self, medicine_data):
        """ Thêm thuốc mới vào cơ sở dữ liệu """
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return False
        if self.validate_medicine_data(medicine_data):
            cursor = self.connection.cursor()
            
            # Lấy ID thuốc mới
            new_id = self.get_next_available_id()

            sql = """
            INSERT INTO thuoc (id, ten_thuoc, mo_ta, don_vi, gia, han_su_dung, so_luong)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(sql, (
                    new_id, medicine_data["Tên thuốc"], medicine_data["Mô tả"], medicine_data["Đơn vị"],
                    medicine_data["Giá"], medicine_data["Hạn sử dụng"], medicine_data["Số lượng"]
                ))
                self.connection.commit()
                return True
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm thuốc: {e}")
                return False
            finally:
                cursor.close()

    def update_medicine(self, medicine_id, medicine_data):
        """ Cập nhật thông tin thuốc """
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return False
        if not medicine_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thuốc để cập nhật!")
            return False
        if self.validate_medicine_data(medicine_data):
            cursor = self.connection.cursor()

            sql = """
            UPDATE thuoc
            SET ten_thuoc = %s, mo_ta = %s, don_vi = %s, gia = %s, han_su_dung = %s, so_luong = %s
            WHERE id = %s
            """
            try:
                cursor.execute(sql, (
                    medicine_data["Tên thuốc"], medicine_data["Mô tả"], medicine_data["Đơn vị"],
                    medicine_data["Giá"], medicine_data["Hạn sử dụng"], medicine_data["Số lượng"], medicine_id
                ))
                self.connection.commit()
                return True
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi cập nhật thuốc: {e}")
                return False
            finally:
                cursor.close()

    def delete_medicine(self, medicine_id):
        """ Xóa thuốc khỏi cơ sở dữ liệu """
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return False
        if not medicine_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thuốc để xóa!")
            return False
        cursor = self.connection.cursor()
        sql = "DELETE FROM thuoc WHERE id = %s"
        try:
            cursor.execute(sql, (medicine_id,))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa thuốc: {e}")
            return False
        finally:
            cursor.close()

    def search_medicine(self, keyword):
        """ Tìm kiếm thuốc theo từ khóa """
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return []
        if not keyword:
            return self.get_all_medicine()
        cursor = self.connection.cursor()
        sql = """
        SELECT id, ten_thuoc, mo_ta, don_vi, gia, han_su_dung, so_luong
        FROM thuoc
        WHERE ten_thuoc LIKE %s OR mo_ta LIKE %s
        """
        try:
            search_pattern = f"%{keyword}%"
            cursor.execute(sql, (search_pattern, search_pattern))
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm thuốc: {e}")
            return []
        finally:
            cursor.close()

    def get_all_medicine(self):
        """ Lấy danh sách tất cả thuốc """
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return []
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, ten_thuoc, mo_ta, don_vi, gia, han_su_dung, so_luong FROM thuoc")
            medicines = cursor.fetchall()
            return medicines
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách thuốc: {e}")
            return []
        finally:
            cursor.close()
