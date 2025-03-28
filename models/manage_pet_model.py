# models/manage_pet_model.py
import mysql.connector
from tkinter import messagebox

class PetModel:
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

    def validate_pet_data(self, pet_data):
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
        try:
            int(pet_data["ID chủ vật nuôi"])
        except ValueError:
            messagebox.showerror("Lỗi", "ID chủ vật nuôi phải là số nguyên!")
            return False
        return True

    def add_pet(self, pet_data):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return False
        if self.validate_pet_data(pet_data):
            cursor = self.connection.cursor()
            sql = """
            INSERT INTO thu_cung (ten, loai, tuoi, gioi_tinh, id_chu_so_huu)
            VALUES (%s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(sql, (
                    pet_data["Tên vật nuôi"], pet_data["Loài"],
                    pet_data["Tuổi"], pet_data["Giới tính"], pet_data["ID chủ vật nuôi"]
                ))
                self.connection.commit()
                return True
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi thêm thú cưng: {e}")
                return False
            finally:
                cursor.close()

    def delete_pet(self, pet_id):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return False
        if not pet_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thú cưng để xóa!")
            return False
        cursor = self.connection.cursor()
        sql = "DELETE FROM thu_cung WHERE id = %s"
        try:
            cursor.execute(sql, (pet_id,))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa thú cưng: {e}")
            return False
        finally:
            cursor.close()

    def update_pet(self, pet_id, pet_data):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return False
        if not pet_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thú cưng để cập nhật!")
            return False
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
                    pet_data["Giới tính"], pet_data["ID chủ vật nuôi"], pet_id
                ))
                self.connection.commit()
                return True
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi cập nhật thú cưng: {e}")
                return False
            finally:
                cursor.close()

    def search_pets(self, keyword):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return []
        if not keyword:
            return self.get_all_pets()
        cursor = self.connection.cursor()
        sql = """
        SELECT id, ten, loai, tuoi, gioi_tinh, id_chu_so_huu 
        FROM thu_cung 
        WHERE ten LIKE %s OR loai LIKE %s OR tuoi LIKE %s OR gioi_tinh LIKE %s
        """
        try:
            search_pattern = f"%{keyword}%"
            cursor.execute(sql, (search_pattern, search_pattern, search_pattern, search_pattern))
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {e}")
            return []
        finally:
            cursor.close()

    def get_all_pets(self):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return []
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, ten, loai, tuoi, gioi_tinh, id_chu_so_huu FROM thu_cung")
            pets = cursor.fetchall()
            return pets
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách: {e}")
            return []
        finally:
            cursor.close()