from customtkinter import *
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from customtkinter import CTkLabel as CLabel
from customtkinter import CTkEntry as CEntry
from customtkinter import CTkButton as CButton
from customtkinter import CTk
from tkinter import messagebox
from PIL import Image 
from customtkinter import CTkImage
from controllers import login_controller
  # Import file xử lý đăng nhập
from views import main_view # Import giao diện chính

# Hàm mở giao diện chính sau khi đăng nhập thành công
def open_home():
    main_view.open_home()

# Tạo cửa sổ đăng nhập
root = CTk()
root.title("Đăng nhập hệ thống")
root.geometry("930x478")

# Thêm ảnh thú cưng (logo)
image = CTkImage(Image.open("./image/login2.jpeg"), size=(930, 478))
imagelabel = CLabel(root, image=image)
imagelabel.place(x=0, y=0)

# Đổi màu nền của cửa sổ
root.configure(fg_color="#ecf0f1")

headinglabel = CLabel(root, text="Hệ thống quản lý thú cưng", bg_color='#FAFAFA', text_color='darkblue', font=('goudy old style', 20, 'bold'))
headinglabel.place(x=20, y=100)

# Ô nhập username & password
usernameEntry = CEntry(root, placeholder_text='Nhập tên đăng nhập', width=180)
usernameEntry.place(x=50, y=150)
passwordEntry = CEntry(root, placeholder_text='Nhập mật khẩu', show='*', width=180)
passwordEntry.place(x=50, y=200)

# Nút đăng nhập
loginButton = CButton(root, text="Đăng nhập", cursor="hand2",
                      command=lambda: login_controller.login(usernameEntry.get(), passwordEntry.get(), root, open_home))
loginButton.place(x=70, y=250)

if __name__ == "__main__":  
    root.mainloop()  # Chạy giao diện login
