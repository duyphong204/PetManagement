# manage_pet.py

from customtkinter import *
from PIL import Image
from tkinter import ttk
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from controllers.manage_pet_controller import add_pet, delete_pet, update_pet, search_pets, get_all_pets

def setup_treeview(parent):
    """Hàm tạo và cấu hình Treeview trong giao diện"""
    style = ttk.Style()
    style.configure("Treeview", font=('Arial', 14))
    style.configure("Treeview.Heading", font=('Arial', 16, 'bold'))

    treeFrame = CTkFrame(parent, fg_color='#161C30')
    treeFrame.grid(row=1, column=0, columnspan=7, pady=10, sticky="nsew")

    tree = ttk.Treeview(treeFrame, height=20)
    tree.grid(row=0, column=0, sticky="nsew")

    # Cấu hình các cột
    columns = ["col_id", "col_ten", "col_loai", "col_tuoi", "col_gioitinh", "col_idchu"]
    headers = ["ID vật nuôi", "Tên vật nuôi", "Loài", "Tuổi", "Giới tính", "ID chủ vật nuôi"]
    
    tree["columns"] = columns
    tree.column("#0", width=0, stretch=False)
    tree.heading("#0", text="")

    for col, header in zip(columns, headers):
        tree.heading(col, text=header)
        tree.column(col, anchor="center", width=120 if col != "col_ten" else 250)

    # Thêm scrollbar
    scrollbar = ttk.Scrollbar(treeFrame, orient=VERTICAL, command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    return tree


def open_manage_pet():
    window = CTkToplevel()  # Tạo cửa sổ con mới
    window.geometry('930x580')
    window.resizable(False, False)
    window.title('Quản lý vật nuôi')
    window.configure(fg_color='#161C30')

    # Logo
    try:
        logo = CTkImage(Image.open('./image/logo6.jpeg'), size=(930, 158))
    except Exception as e:
        print(f"Lỗi khi tải hình ảnh: {e}")
        return

    CTkLabel(window, image=logo, text='').grid(row=0, column=0, columnspan=2)

    # Left Frame - Form nhập liệu
    leftFrame = CTkFrame(window, fg_color='#161C30')
    leftFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

    labels = ["ID vật nuôi", "Tên vật nuôi", "Loài", "Tuổi", "Giới tính", "ID chủ vật nuôi"]
    entries = {}

    for i, label in enumerate(labels):
        CTkLabel(leftFrame, text=label, font=('Arial', 18, 'bold')).grid(row=i, column=0, padx=20, pady=10)
        
        if label == "Giới tính":
            entries[label] = CTkComboBox(leftFrame, values=["Đực", "Cái"], width=140)
        else:
            entries[label] = CTkEntry(leftFrame, font=('Arial', 15), width=140)
        
        entries[label].grid(row=i, column=1, pady=5)

    # Right Frame - Treeview và tìm kiếm
    rightFrame = CTkFrame(window, fg_color='#161C30')
    rightFrame.grid(row=1, column=1, padx=10, pady=10, sticky="ne")

    search_options = ["id", "ten", "loai", "tuoi", "gioi_tinh", "id_chu"]
    searchbox = CTkComboBox(rightFrame, values=search_options, width=140)
    searchbox.set("Tìm kiếm theo")
    searchbox.grid(row=0, column=0)

    searchEntry = CTkEntry(rightFrame, width=140, placeholder_text="Nhập từ khóa...")
    searchEntry.grid(row=0, column=1, padx=5)

    CTkButton(rightFrame, text='Tìm kiếm', width=80, command=lambda: on_search(tree, searchbox.get(), searchEntry.get())).grid(row=0, column=2, padx=5)
    CTkButton(rightFrame, text='Show all', width=80, command=lambda: show_all(tree)).grid(row=0, column=3, padx=5)

    # Treeview
    tree = setup_treeview(rightFrame)

    # Button Frame - Các chức năng
    buttonFrame = CTkFrame(window, fg_color='#161C30')
    buttonFrame.grid(row=2, column=0, columnspan=2, pady=10)

    buttons = ["Thêm mới", "Sửa", "Xoá"]
    button_commands = [lambda: on_add(entries, tree), lambda: on_update(entries, tree), lambda: on_delete(tree)]
    for i, (text, command) in enumerate(zip(buttons, button_commands)):
        CTkButton(buttonFrame, text=text, font=('Arial', 15, 'bold'), width=160, command=command).grid(row=0, column=i, padx=10, pady=5)

    window.mainloop()

def on_add(entries, tree):
    pet = {label: entry.get() for label, entry in entries.items()}
    add_pet(pet)
    refresh_tree(tree)

def on_update(entries, tree):
    pet = {label: entry.get() for label, entry in entries.items()}
    update_pet(pet)
    refresh_tree(tree)

def on_delete(tree):
    selected_item = tree.selection()[0]
    pet_id = tree.item(selected_item, "values")[0]
    delete_pet(pet_id)
    refresh_tree(tree)

def on_search(tree, field, keyword):
    results = search_pets(keyword, field)
    refresh_tree(tree, results)

def show_all(tree):
    pets = get_all_pets()
    refresh_tree(tree, pets)

def refresh_tree(tree, pets=None):
    if pets is None:
        pets = get_all_pets()
