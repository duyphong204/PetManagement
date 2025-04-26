import mysql.connector
from tkinter import messagebox
from datetime import datetime

class InvoiceModel:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="qlthucung"
            )
            print("Kết nối cơ sở dữ liệu thành công!")
        except mysql.connector.Error as e:
            messagebox.showwarning("Lỗi kết nối", f"Không thể kết nối đến cơ sở dữ liệu: {e}")

    def validate_invoice_data(self, invoice_data):
        if not invoice_data.get("id_chu_so_huu"):
            messagebox.showwarning("Cảnh báo", "ID Chủ sở hữu không được để trống!")
            return False
        if not invoice_data.get("tong_tien"):
            messagebox.showwarning("Cảnh báo", "Tổng tiền không được để trống!")
            return False
        if not invoice_data.get("ngay_tao"):
            messagebox.showwarning("Cảnh báo", "Ngày tạo không được để trống!")
            return False
        if not invoice_data.get("trang_thai"):
            messagebox.showwarning("Cảnh báo", "Trạng thái không được để trống!")
            return False
        return True

    def check_owner_exists(self, owner_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM chu_so_huu WHERE id = %s", (owner_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def add_invoice(self, invoice_data):
        if not self.validate_invoice_data(invoice_data):
            return
        if not self.check_owner_exists(invoice_data["id_chu_so_huu"]):
            messagebox.showwarning("Cảnh báo", f"Chủ sở hữu với ID {invoice_data['id_chu_so_huu']} không tồn tại!")
            return
        cursor = self.connection.cursor()
        sql = """
        INSERT INTO hoa_don (id_chu_so_huu, tong_tien, ngay_tao, trang_thai)
        VALUES (%s, %s, %s, %s)
        """
        try:
            cursor.execute(sql, (
                invoice_data["id_chu_so_huu"],
                invoice_data["tong_tien"],
                invoice_data["ngay_tao"],
                invoice_data["trang_thai"]
            ))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Thêm hóa đơn thành công!")
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm hóa đơn: {e}")
        finally:
            cursor.close()

    def delete_invoice(self, id):
        if not id:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn để xóa!")
            return
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM hoa_don WHERE id = %s", (id,))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Xóa hóa đơn thành công!")
        except mysql.connector.Error as e:
            messagebox.showwarning("Lỗi", f"Lỗi khi xóa hóa đơn: {e}")
        finally:
            cursor.close()

    def update_invoice(self, invoice_data):
        if not self.validate_invoice_data(invoice_data):
            return
        if not self.check_owner_exists(invoice_data["id_chu_so_huu"]):
            messagebox.showwarning("Cảnh báo", f"Chủ sở hữu với ID {invoice_data['id_chu_so_huu']} không tồn tại!")
            return
        cursor = self.connection.cursor()
        sql = """
        UPDATE hoa_don
        SET id_chu_so_huu = %s, tong_tien = %s, ngay_tao = %s, trang_thai = %s
        WHERE id = %s
        """
        try:
            cursor.execute(sql, (
                invoice_data["id_chu_so_huu"],
                invoice_data["tong_tien"],
                invoice_data["ngay_tao"],
                invoice_data["trang_thai"],
                invoice_data["id"]
            ))
            self.connection.commit()
            messagebox.showinfo("Thành công", "Cập nhật hóa đơn thành công!")
        except mysql.connector.Error as e:
            messagebox.showwarning("Lỗi", f"Lỗi khi cập nhật hóa đơn: {e}")
        finally:
            cursor.close()

    def get_all_invoices(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT id, id_chu_so_huu, tong_tien, ngay_tao, trang_thai FROM hoa_don ORDER BY id ")
            invoices = cursor.fetchall()
            if not invoices:
                messagebox.showinfo("Thông báo", "Không có dữ liệu hóa đơn trong CSDL!")
            return invoices
        except mysql.connector.Error as e:
            messagebox.showwarning("Lỗi", f"Lỗi khi lấy danh sách: {e}")
            return []
        finally:
            cursor.close()

    def delete_all_invoices(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("DELETE FROM hoa_don")
            self.connection.commit()
            messagebox.showinfo("Thành công", "Đã xóa tất cả hóa đơn!")
        except mysql.connector.Error as e:
            messagebox.showwarning("Lỗi", f"Lỗi khi xóa tất cả: {e}")
        finally:
            cursor.close()

    def search_invoices(self, conditions):
        """
        Tìm kiếm hóa đơn theo ngày và từ khóa.
        Nếu bất kỳ trường nào khớp với từ khóa hoặc nằm trong khoảng ngày, kết quả sẽ được trả về.
        """
        if not conditions:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập ít nhất một điều kiện tìm kiếm!")
            return []

        cursor = self.connection.cursor()
        try:
            sql = """
            SELECT id, id_chu_so_huu, tong_tien, ngay_tao, trang_thai
            FROM hoa_don
            WHERE 1=1
            """
            params = []

            # Thêm điều kiện tìm kiếm theo ngày
            if "ngay_tao >=" in conditions and conditions["ngay_tao >="]:
                sql += " AND ngay_tao >= %s"
                params.append(conditions["ngay_tao >="])
            if "ngay_tao <=" in conditions and conditions["ngay_tao <="]:
                sql += " AND ngay_tao <= %s"
                params.append(conditions["ngay_tao <="])

            # Thêm điều kiện tìm kiếm theo từ khóa
            if "keyword" in conditions and conditions["keyword"]:
                keyword = f"%{conditions['keyword']}%"
                sql += """
                AND (
                    CAST(id AS CHAR) LIKE %s OR
                    CAST(id_chu_so_huu AS CHAR) LIKE %s OR
                    trang_thai LIKE %s
                )
                """
                params.extend([keyword, keyword, keyword])

            sql += " ORDER BY ngay_tao DESC"

            # Debug thông tin truy vấn
            print("SQL Query:", sql)
            print("Parameters:", params)

            cursor.execute(sql, tuple(params))
            results = cursor.fetchall()

            # Chuyển đổi kết quả thành danh sách dictionary
            invoices = [
                {
                    "id": row[0],
                    "id_chu_so_huu": row[1],
                    "tong_tien": row[2],
                    "ngay_tao": row[3],
                    "trang_thai": row[4]
                }
                for row in results
            ]

            if not invoices:
                messagebox.showinfo("Thông báo", "Không tìm thấy kết quả phù hợp")
            return invoices
        except mysql.connector.Error as e:
            messagebox.showerror("Lỗi", f"Lỗi database: {str(e)}")
            return []
        finally:
            cursor.close()
