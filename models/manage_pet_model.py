import mysql.connector
from tkinter import messagebox

class PetModel:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="qlthucung"
        )

    def validate_pet_data(self, pet_data):
        """Kiểm tra dữ liệu thú cưng trước khi thêm hoặc sửa"""
        if not pet_data["ID vật nuôi"]:
            messagebox.showerror("Lỗi", "ID vật nuôi không được để trống!")
            return False
        if not pet_data["Tên vật nuôi"]:
            messagebox.showerror("Lỗi", "Tên vật nuôi không được để trống!")
            return False
        if not pet_data["Loài"]:
            messagebox.showerror("Lỗi", "Loài không được để trống!")
            return False
        if not pet_data["Tuổi"]:
            messagebox.showerror("Lỗi", "Tuổi không được để trống!")
            return False
        try:
            int(pet_data["Tuổi"])
        except ValueError:
            messagebox.showerror("Lỗi", "Tuổi phải là số nguyên!")
            return False
        if not pet_data["Giới tính"]:
            messagebox.showerror("Lỗi", "Giới tính không được để trống!")
            return False
        if not pet_data["ID chủ vật nuôi"]:
            messagebox.showerror("Lỗi", "ID chủ vật nuôi không được để trống!")
            return False
        return True

    def add_pet(self, pet_data):
        """Thêm một vật nuôi mới vào bảng thu_cung."""
        if self.validate_pet_data(pet_data):
            cursor = self.connection.cursor()
            sql = """
            INSERT INTO thu_cung (id, ten, loai, tuoi, gioi_tinh, id_chu_so_huu)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(sql, (
                    pet_data["ID vật nuôi"], pet_data["Tên vật nuôi"], pet_data["Loài"],
                    pet_data["Tuổi"], pet_data["Giới tính"], pet_data["ID chủ vật nuôi"]
                ))
                self.connection.commit()
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm thú cưng: {e}")
            finally:
                cursor.close()

    def delete_pet(self, pet_id):
        """Xóa một vật nuôi khỏi bảng thu_cung bằng ID."""
        if not pet_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thú cưng để xóa!")
            return
        cursor = self.connection.cursor()
        sql = "DELETE FROM thu_cung WHERE id = %s"
        try:
            cursor.execute(sql, (pet_id,))
            self.connection.commit()
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa thú cưng: {e}")
        finally:
            cursor.close()

    def update_pet(self, pet_data):
        """Cập nhật thông tin của một vật nuôi."""
        if self.validate_pet_data(pet_data):
            cursor = self.connection.cursor()
            sql = """
            UPDATE thu_cung
            SET ten = %s, loai = %s, tuoi = %s, gioi_tinh = %s, id_chu_so_huu = %s
            WHERE id = %s
            """
            try:
                cursor.execute(sql, (
                    pet_data["Tên vật nuôi"], pet_data["Loài"], pet_data["Tuổi"],
                    pet_data["Giới tính"], pet_data["ID chủ vật nuôi"], pet_data["ID vật nuôi"]
                ))
                self.connection.commit()
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi cập nhật thú cưng: {e}")
            finally:
                cursor.close()

    def search_pets(self, keyword, field):
        """Tìm kiếm vật nuôi theo một trường cụ thể."""
        if not keyword or not field:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập từ khóa và chọn trường tìm kiếm!")
            return []
        cursor = self.connection.cursor()
        sql = f"SELECT * FROM thu_cung WHERE {field} LIKE %s"
        try:
            cursor.execute(sql, ('%' + keyword + '%',))
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {e}")
            return []
        finally:
            cursor.close()

    def get_all_pets(self):
        """Lấy danh sách tất cả vật nuôi trong hệ thống."""
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM thu_cung")
            pets = cursor.fetchall()
            if not pets:
                messagebox.showinfo("Thông báo", "Không có dữ liệu thú cưng trong CSDL!")
            return pets
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách: {e}")
            return []
        finally:
            cursor.close()

    def delete_all_pets(self):
        """Xóa tất cả thú cưng"""
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM thu_cung")
            self.connection.commit()
            messagebox.showinfo("Thành công", "Đã xóa tất cả thú cưng!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa tất cả: {e}")
        finally:
            cursor.close()

    def __del__(self):
        """Đóng kết nối khi đối tượng bị hủy."""
        if self.connection.is_connected():
            self.connection.close()