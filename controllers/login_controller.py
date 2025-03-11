import mysql.connector
from tkinter import messagebox
from utils.connect_dtb import connect_db

def login(username, password, root, open_main_callback):
    if username == '' or password == '':
        messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không được để trống!")
        return
    
    try:
        conn = connect_db()  # Kết nối đến database
        cursor = conn.cursor()

        # Kiểm tra tài khoản trong bảng nguoi dùng 
        query = "SELECT * FROM nguoi_dung WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
            root.destroy()  # Đóng cửa sổ đăng nhập
            open_main_callback()  # Gọi hàm mở giao diện chính
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu sai!")

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        messagebox.showerror("Lỗi kết nối CSDL", f"Lỗi: {e}")
