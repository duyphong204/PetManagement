import mysql.connector
from tkinter import messagebox
from tkinter import ttk

class DrugModel:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="qlthucung2"  # Đổi sang qlthucung2
            )
            print("Kết nối CSDL thành công!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối CSDL: {e}")
            self.connection = None

    def get_medicine_names_by_kho_thuoc_id(self, id_kho_thuoc):
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return []
        if id_kho_thuoc is None:
            # Nếu không có id_kho_thuoc, lấy tất cả ten_thuoc từ kho_thuoc
            cursor = self.connection.cursor()
            sql = "SELECT ten_thuoc FROM kho_thuoc"
            try:
                cursor.execute(sql)
                medicines = cursor.fetchall()
                return [medicine[0] for medicine in medicines]  # Trả về danh sách tên thuốc
            except mysql.connector.Error as e:
                messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách tên thuốc: {e}")
                return []
            finally:
                cursor.close()

        # Kiểm tra xem id_kho_thuoc có tồn tại trong bảng thuoc và liên kết với kho_thuoc
        cursor = self.connection.cursor()
        sql = """
        SELECT DISTINCT kho_thuoc.ten_thuoc 
        FROM kho_thuoc 
        JOIN thuoc ON kho_thuoc.id = thuoc.id_kho_thuoc 
        WHERE thuoc.id_kho_thuoc = %s
        """
        try:
            cursor.execute(sql, (id_kho_thuoc,))
            medicines = cursor.fetchall()
            return [medicine[0] for medicine in medicines]  # Trả về danh sách tên thuốc
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách tên thuốc: {e}")
            return []
        finally:
            cursor.close()

    def get_kho_thuoc_id_by_name(self, ten_thuoc):
        """Lấy id từ bảng kho_thuoc dựa trên ten_thuoc"""
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return None
        cursor = self.connection.cursor()
        sql = "SELECT id FROM kho_thuoc WHERE ten_thuoc = %s"
        try:
            cursor.execute(sql, (ten_thuoc,))
            result = cursor.fetchone()
            if result:
                return result[0]  # Trả về id của kho_thuoc
            else:
                messagebox.showerror("Lỗi", f"Tên thuốc '{ten_thuoc}' không tồn tại trong kho thuốc!")
                return None
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy ID kho thuốc: {e}")
            return None
        finally:
            cursor.close()

    def validate_medicine_data(self, medicine_data):
        # Kiểm tra tên thuốc không được để trống
        if not medicine_data["Tên thuốc"]:
            messagebox.showerror("Lỗi", "Tên thuốc không được để trống!")
            return False

        # Kiểm tra loại thuốc không được để trống
        if not medicine_data["Loại thuốc"]:
            messagebox.showerror("Lỗi", "Loại thuốc không được để trống!")
            return False

        # Kiểm tra giá trị giá không âm
        try:
            gia = float(medicine_data["Giá"])
            if gia < 0:
                messagebox.showerror("Lỗi", "Giá không được nhỏ hơn 0!")
                return False
        except ValueError:
            messagebox.showerror("Lỗi", "Giá phải là một số hợp lệ!")
            return False

        return True

    def add_medicine(self, medicine_data, kho_thuoc_id):
        """Thêm thuốc mới vào cơ sở dữ liệu"""
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return False

        # Kiểm tra các điều kiện cơ bản
        if not self.validate_medicine_data(medicine_data):
            return False

        # Kiểm tra tên thuốc có bị trùng không (chỉ khi thêm mới)
        cursor = self.connection.cursor()
        sql = "SELECT COUNT(*) FROM thuoc WHERE ten_thuoc = %s"
        try:
            cursor.execute(sql, (medicine_data["Tên thuốc"],))
            count = cursor.fetchone()[0]
            if count > 0:
                messagebox.showerror("Lỗi", "Tên thuốc đã tồn tại trong cơ sở dữ liệu!")
                return False
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi kiểm tra tên thuốc: {e}")
            return False
        finally:
            cursor.close()

        # Thêm thuốc vào cơ sở dữ liệu
        cursor = self.connection.cursor()
        sql = """
        INSERT INTO thuoc (ten_thuoc, loai_thuoc, nha_san_xuat, gia, id_kho_thuoc)
        VALUES (%s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (
                medicine_data["Tên thuốc"], medicine_data["Loại thuốc"],
                medicine_data["Nhà sản xuất"], medicine_data["Giá"], kho_thuoc_id
            ))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Thêm thuốc thành công!")
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm thuốc: {e}")
            return False
        finally:
            cursor.close()

    def update_medicine(self, medicine_id, medicine_data, kho_thuoc_id):
        """Cập nhật thông tin thuốc - Không kiểm tra trùng tên thuốc"""
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return False
        if not medicine_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thuốc để cập nhật!")
            return False

        # Kiểm tra các điều kiện cơ bản (không kiểm tra trùng tên)
        if not self.validate_medicine_data(medicine_data):
            return False

        # Cập nhật thông tin thuốc
        cursor = self.connection.cursor()
        sql = """
        UPDATE thuoc
        SET ten_thuoc = %s, loai_thuoc = %s, nha_san_xuat = %s, gia = %s, id_kho_thuoc = %s
        WHERE id = %s
        """
        try:
            cursor.execute(sql, (
                medicine_data["Tên thuốc"], medicine_data["Loại thuốc"],
                medicine_data["Nhà sản xuất"], medicine_data["Giá"], kho_thuoc_id, medicine_id
            ))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Cập nhật thuốc thành công!")
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật thuốc: {e}")
            return False
        finally:
            cursor.close()

    def delete_medicine(self, medicine_id):
        """Xóa thuốc khỏi cơ sở dữ liệu"""
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
            messagebox.showinfo("Thành công", "Xóa thuốc thành công!")
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa thuốc: {e}")
            return False
        finally:
            cursor.close()

    def search_medicine(self, keyword, field):
        """Tìm kiếm thuốc theo từ khóa và trường cụ thể"""
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return []
        if not keyword or not field:
            return self.get_all_medicine()
        cursor = self.connection.cursor()
        field_mapping = {
            "Tên thuốc": "ten_thuoc",
            "Loại thuốc": "loai_thuoc",
            "Nhà sản xuất": "nha_san_xuat",
            "Giá": "gia"
        }
        db_field = field_mapping.get(field, "ten_thuoc")
        sql = f"""
        SELECT id, ten_thuoc, loai_thuoc, nha_san_xuat, gia
        FROM thuoc
        WHERE {db_field} LIKE %s
        """
        try:
            search_pattern = f"%{keyword}%"
            cursor.execute(sql, (search_pattern,))
            results = cursor.fetchall()
            return results
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm thuốc: {e}")
            return []
        finally:
            cursor.close()

    def get_all_medicine(self):
        """Lấy danh sách tất cả thuốc"""
        if not self.connection:
            messagebox.showerror("Lỗi", "Không thể kết nối CSDL!")
            return []
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, ten_thuoc, loai_thuoc, nha_san_xuat, gia FROM thuoc")
            medicines = cursor.fetchall()
            if not medicines:
                messagebox.showinfo("Thông báo", "Không có thuốc nào trong danh sách!")
            return medicines
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách thuốc: {e}")
            return []
        finally:
            cursor.close()

    def __del__(self):
        """Đóng kết nối khi đối tượng bị hủy"""
        if self.connection and self.connection.is_connected():
            self.connection.close()