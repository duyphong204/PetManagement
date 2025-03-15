import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
from models.login_model import LoginModel  # Import từ tầng logic
from views import main_view

# Hàm mở giao diện chính sau khi đăng nhập thành công
def open_home(root):
    main_view.open_home()  # Mở giao diện chính

# Tạo cửa sổ đăng nhập
root = Tk()
root.title("Đăng nhập hệ thống")
root.geometry("925x500+300+200")
root.configure(bg="#fff")
root.resizable(False, False)

# Khởi tạo LoginModel
login_model = LoginModel()

# Thêm ảnh thú cưng (logo)
image = PhotoImage(file="image/login.png")
Label(root, image=image, bg='white').place(x=50, y=50)

# Khung chứa thông tin đăng nhập
frame = Frame(root, width=350, height=350, bg='white')
frame.place(x=480, y=70)

heading = Label(frame, text="Sign in", fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)

# Xử lý nhập username
def on_enter_user(event):
    user.delete(0, END)

def on_leave_user(event):
    if user.get() == "":
        user.insert(0, "Username")

user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, "Username")
user.bind("<FocusIn>", on_enter_user)
user.bind("<FocusOut>", on_leave_user)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

# Xử lý nhập password
def on_enter_pass(event):
    password.delete(0, END)
    password.config(show="*")  # Ẩn mật khẩu

def on_leave_pass(event):
    if password.get() == "":
        password.insert(0, "Password")
        password.config(show="")  # Hiện lại chữ 'Password' khi ô trống

password = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Microsoft YaHei UI Light', 11))
password.place(x=30, y=150)
password.insert(0, "Password")
password.bind("<FocusIn>", on_enter_pass)
password.bind("<FocusOut>", on_leave_pass)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

# Xử lý đăng nhập
def handle_login():
    username = user.get()
    pwd = password.get()
    success = login_model.login(username, pwd, root, open_home)  # Gọi từ tầng logic
    if not success:
        messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không chính xác!")

# Nút đăng nhập
Button(frame, width=39, pady=7, text='Sign in', bg='#57a1f8', fg='white', border=0, command=handle_login).place(x=35, y=204)

# Nhãn và nút đăng ký
Label(frame, text="Don't have an account?", bg='white', fg='#57a1f8', font=('Microsoft YaHei UI Light', 9)).place(x=75, y=270)
sign_up = Button(frame, width=6, text='Sign up', border=0, bg='white', cursor='hand2', fg='#57a1f8')
sign_up.place(x=215, y=270)

root.mainloop()