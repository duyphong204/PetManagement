from customtkinter import *
from customtkinter import CTkLabel as CLabel
from customtkinter import CTkEntry as CEntry
from customtkinter import CTkButton as CButton
from customtkinter import CTk
from tkinter import messagebox
from PIL import Image 
from customtkinter import CTkImage
import main_view
# from utils.connect_dtb import connect_db  # Đảm bảo có file connect_dtb.py với hàm connect_db()
# # Kết nối đến database
# conn = connect_db()
# cursor = conn.cursor()

def login():
    global usernameEntry, passwordEntry
    if usernameEntry.get()=='' or passwordEntry.get()== '':
        messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không được để trống!")
    elif usernameEntry.get()=='admin' and passwordEntry.get()=='123':
        messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
        root.destroy()  # Đóng cửa sổ đăng nhập
    else:
        messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu sai!")


root = CTk()
root.title("Đăng nhập hệ thống")
root.geometry("930x478")

# Thêm ảnh thú cưng (logo)
image = CTkImage(Image.open("./image/login2.jpeg"),size=(930,478))
imagelabel = CLabel(root, image=image)
imagelabel.place(x=0,y=0)

# Đổi màu nền của cửa sổ (CustomTkinter không dùng bg)
root.configure(fg_color="#ecf0f1")

headinglabel = CLabel(root, text="Hệ thống quản lý thú cưng", bg_color='#FAFAFA', text_color='darkblue',font=('goudy old style ',20,'bold'))
headinglabel.place(x=20,y=100)

# username and password labels
usernameEntry = CEntry(root, placeholder_text='Nhập tên đăng nhập',width=180)
usernameEntry.place(x=50, y=150)
passwordEntry = CEntry(root, placeholder_text='Nhập mật khẩu', show='*',width=180)
passwordEntry.place(x=50, y=200)

# login button
loginButton = CButton(root, text="Đăng nhập", cursor="hand2",command=login)
loginButton.place(x=70, y=250)

root.mainloop()
