import mysql.connector
from tkinter import messagebox

class UserModel:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="qlthucung2"
            )
            print("Kết nối CSDL người dùng thành công!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Không thể kết nối CSDL: {e}")
            self.connection = None

    def validate_user_data(self, data):
        if not data["Tên đăng nhập"]:
            messagebox.showerror("Lỗi", "Tên đăng nhập không được để trống.")
            return False

        if not data["Mật khẩu"]:
            messagebox.showerror("Lỗi", "Mật khẩu không được để trống.")
            return False

        if not data["Email"] or "@" not in data["Email"] or "." not in data["Email"]:
            messagebox.showerror("Lỗi", "Email không hợp lệ.")
            return False

        if data["Quyền"].lower() not in ["admin", "bac_si", "khach_hang", "none"]:
            messagebox.showerror("Lỗi", "Quyền không hợp lệ.")
            return False

        return True

    def is_duplicate_username(self, username, exclude_id=None):
        try:
            cursor = self.connection.cursor()
            if exclude_id:
                cursor.execute("SELECT COUNT(*) FROM nguoi_dung WHERE username = %s AND id != %s", (username, exclude_id))
            else:
                cursor.execute("SELECT COUNT(*) FROM nguoi_dung WHERE username = %s", (username,))
            return cursor.fetchone()[0] > 0
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi kiểm tra trùng tên đăng nhập: {e}")
            return True
        finally:
            cursor.close()

    def is_duplicate_email(self, email, exclude_id=None):
        try:
            cursor = self.connection.cursor()
            if exclude_id:
                cursor.execute("SELECT COUNT(*) FROM nguoi_dung WHERE email = %s AND id != %s", (email, exclude_id))
            else:
                cursor.execute("SELECT COUNT(*) FROM nguoi_dung WHERE email = %s", (email,))
            return cursor.fetchone()[0] > 0
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi kiểm tra trùng email: {e}")
            return True
        finally:
            cursor.close()

    def get_all_users(self):
        if not self.connection:
            return []
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, username, password, email, IFNULL(role, 'none') FROM nguoi_dung")
            return cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy danh sách người dùng: {e}")
            return []
        finally:
            cursor.close()

    def add_user(self, data):
        if not self.connection:
            return False
        if not self.validate_user_data(data):
            return False

        if self.is_duplicate_username(data["Tên đăng nhập"]):
            messagebox.showwarning("Trùng tên đăng nhập", "Tên đăng nhập đã tồn tại.")
            return False

        if self.is_duplicate_email(data["Email"]):
            messagebox.showwarning("Trùng Email", "Email đã tồn tại.")
            return False

        role = None if data["Quyền"] == "none" else data["Quyền"]

        try:
            cursor = self.connection.cursor()
            sql = "INSERT INTO nguoi_dung (id, username, password, email, role) VALUES (%s, %s, %s, %s, %s)"
            next_id = self.get_next_available_id()
            cursor.execute(sql, (next_id, data["Tên đăng nhập"], data["Mật khẩu"], data["Email"], role))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm người dùng: {e}")
            return False
        finally:
            cursor.close()

    def update_user(self, user_id, data):
        if not self.connection:
            return False
        if not self.validate_user_data(data):
            return False

        if self.is_duplicate_username(data["Tên đăng nhập"], exclude_id=user_id):
            messagebox.showwarning("Trùng tên đăng nhập", "Tên đăng nhập đã tồn tại ở người dùng khác.")
            return False

        if self.is_duplicate_email(data["Email"], exclude_id=user_id):
            messagebox.showwarning("Trùng Email", "Email đã tồn tại ở người dùng khác.")
            return False

        role = None if data["Quyền"] == "none" else data["Quyền"]

        try:
            cursor = self.connection.cursor()
            sql = """
                UPDATE nguoi_dung
                SET username = %s, password = %s, email = %s, role = %s
                WHERE id = %s
            """
            cursor.execute(sql, (data["Tên đăng nhập"], data["Mật khẩu"], data["Email"], role, user_id))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật người dùng: {e}")
            return False
        finally:
            cursor.close()

    def delete_user(self, user_id):
        if not self.connection:
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM nguoi_dung WHERE id = %s", (user_id,))
            self.connection.commit()
            return True
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa người dùng: {e}")
            return False
        finally:
            cursor.close()

    def search_user(self, keyword):
        if not self.connection:
            return []
        try:
            cursor = self.connection.cursor()
            pattern = f"%{keyword}%"
            sql = """
                SELECT id, username, password, email, IFNULL(role, 'none')
                FROM nguoi_dung
                WHERE username LIKE %s OR email LIKE %s OR role LIKE %s
            """
            cursor.execute(sql, (pattern, pattern, pattern))
            return cursor.fetchall()
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm người dùng: {e}")
            return []
        finally:
            cursor.close()

    def get_next_available_id(self):
        if not self.connection:
            return 1
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM nguoi_dung ORDER BY id ASC")
            ids = [row[0] for row in cursor.fetchall()]
            for i in range(1, len(ids) + 2):
                if i not in ids:
                    return i
        except mysql.connector.Error:
            return 1
        finally:
            cursor.close()
