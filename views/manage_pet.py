from customtkinter import * 
from PIL import Image
from tkinter import ttk

window = CTk()
window.geometry('930x580')
window.resizable(False, False)
window.title('Quản lý vật nuôi')
window.configure(fg_color='#161C30')

# Logo
logo = CTkImage(Image.open('./image/logo6.jpeg'), size=(930,158))
logoLabel = CTkLabel(window, image=logo, text='')
logoLabel.grid(row=0, column=0, columnspan=2)

# Frame bên trái
leftFrame = CTkFrame(window, fg_color='#161C30')
leftFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

# id vật nuôi
idLabel = CTkLabel(leftFrame, text='ID vật nuôi', font=('arial', 18, 'bold'))
idLabel.grid(row=0, column=0, padx=20, pady=15)
idEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=140)
idEntry.grid(row=0, column=1)

# tên vật nuôi 
TenLabel = CTkLabel(leftFrame, text='Tên vật nuôi', font=('arial', 18, 'bold'))
TenLabel.grid(row=1, column=0, padx=20, pady=15)
TenEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=140)
TenEntry.grid(row=1, column=1)

# loài vật nuôi 
LoaiLabel = CTkLabel(leftFrame, text='Loài', font=('arial', 18, 'bold'))
LoaiLabel.grid(row=2, column=0, padx=20, pady=15)
LoaiEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=140)
LoaiEntry.grid(row=2, column=1)

# tuổi vật nuôi 
TuoiLabel = CTkLabel(leftFrame, text='Tuổi', font=('arial', 18, 'bold'))
TuoiLabel.grid(row=3, column=0, padx=20, pady=15)
TuoiEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=140)
TuoiEntry.grid(row=3, column=1)

# giới tính vật nuôi 
GTLabel = CTkLabel(leftFrame, text='Giới tính', font=('arial', 18, 'bold'))
GTLabel.grid(row=4, column=0, padx=20, pady=15)
GToptions = ['Đực', 'Cái']
GTbox = CTkComboBox(leftFrame, values=GToptions, width=140)
GTbox.grid(row=4, column=1)

# id chủ vật nuôi 
ID_chuLabel = CTkLabel(leftFrame, text='ID chủ vật nuôi', font=('arial', 18, 'bold'))
ID_chuLabel.grid(row=5, column=0, padx=20, pady=15)
ID_chuEntry = CTkEntry(leftFrame, font=('arial', 15, 'bold'), width=140)
ID_chuEntry.grid(row=5, column=1)

# Frame bên phải
rightFrame = CTkFrame(window, fg_color='#161C30')
rightFrame.grid(row=1, column=1, padx=10, pady=10, sticky="ne")

search_options = ['ID vật nuôi', 'Tên vật nuôi', 'Loài', 'Tuổi', 'Giới tính', 'ID chủ vật nuôi']
searchbox = CTkComboBox(rightFrame, values=search_options, width=140)
searchbox.grid(row=0, column=0)
searchbox.set("Tìm kiếm theo")

searchEntry = CTkEntry(rightFrame, width=140)
searchEntry.grid(row=0, column=1, padx=5)

searchButttom = CTkButton(rightFrame, text='Tìm kiếm', width=80)
searchButttom.grid(row=0, column=2, padx=5)

showallButtton = CTkButton(rightFrame, text='Show all', width=80)
showallButtton.grid(row=0, column=3, padx=5)

# Frame chứa Treeview và scrollbar
treeFrame = CTkFrame(rightFrame, fg_color='#161C30')
treeFrame.grid(row=1, column=0, columnspan=7, pady=10, sticky="nsew")

# Cấu hình Treeview với font chữ lớn hơn
style = ttk.Style()
style.configure("Treeview", font=('arial', 14))
style.configure("Treeview.Heading", font=('arial', 16, 'bold'))

tree = ttk.Treeview(treeFrame, height=20)
tree.grid(row=0, column=0, sticky="nsew")

# Đặt tên cho các cột
tree["columns"] = ("col_id", "col_ten", "col_loai", "col_tuoi", "col_gioitinh", "col_idchu")
tree.column("#0", width=0, stretch=False)
tree.heading("#0", text="")

tree.heading("col_id", text="ID vật nuôi")
tree.heading("col_ten", text="Tên vật nuôi")
tree.heading("col_loai", text="Loài")
tree.heading("col_tuoi", text="Tuổi")
tree.heading("col_gioitinh", text="Giới tính")
tree.heading("col_idchu", text="ID chủ vật nuôi")

tree.column("col_id", anchor=CENTER, width=120)
tree.column("col_ten", anchor=W, width=250)
tree.column("col_loai", anchor=W, width=150)
tree.column("col_tuoi", anchor=CENTER, width=100)
tree.column("col_gioitinh", anchor=CENTER, width=100)
tree.column("col_idchu", anchor=CENTER, width=150)

# Tạo scrollbar và gắn vào Treeview
scrollbar = ttk.Scrollbar(treeFrame, orient=VERTICAL, command=tree.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
tree.configure(yscrollcommand=scrollbar.set)

# Frame chứa các nút chức năng
buttonFrame = CTkFrame(window, fg_color='#161C30')
buttonFrame.grid(row=2, column=0, columnspan=2)
newButtton = CTkButton(buttonFrame, text='Thêm mới', font=('arial', 15, 'bold'), width=160)
newButtton.grid(row=0, column=0, pady=5)
updateButtton = CTkButton(buttonFrame, text='Sửa', font=('arial', 15, 'bold'), width=160)
updateButtton.grid(row=0, column=1, pady=5)
deleteButtton = CTkButton(buttonFrame, text='Xoá', font=('arial', 15, 'bold'), width=160)
deleteButtton.grid(row=0, column=2, pady=5)

window.mainloop()
