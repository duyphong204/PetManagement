import customtkinter as ctk
from models.manage_pet_model import PetModel
from tkinter import messagebox
from tkinter.ttk import Treeview
import controllers.manage_pet_controller as pet_controller

def open_manage_pet_content(frame):
    # Khởi tạo Controller để giao tiếp với tầng logic
    pet_controller_instance = pet_controller.ManagePetController()

    # Tiêu đề
    title_label = ctk.CTkLabel(frame, text="Quản lý Thú cưng", font=("Arial", 18, "bold"))
    title_label.pack(pady=10)

    # Frame chính chứa toàn bộ nội dung
    content_frame = ctk.CTkFrame(frame)
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Frame bên trái: Ô nhập liệu
    input_frame = ctk.CTkFrame(content_frame, width=300)
    input_frame.pack(side="left", padx=10, pady=5, fill="y")

    # Sắp xếp các ô nhập liệu dọc
    ctk.CTkLabel(input_frame, text="ID vật nuôi:", font=("Arial", 12)).pack(pady=5, anchor="w")
    pet_id_entry = ctk.CTkEntry(input_frame, width=250)
    pet_id_entry.pack(pady=5)

    ctk.CTkLabel(input_frame, text="Tên vật nuôi:", font=("Arial", 12)).pack(pady=5, anchor="w")
    pet_name_entry = ctk.CTkEntry(input_frame, width=250)
    pet_name_entry.pack(pady=5)

    ctk.CTkLabel(input_frame, text="Loài:", font=("Arial", 12)).pack(pady=5, anchor="w")
    pet_species_entry = ctk.CTkEntry(input_frame, width=250)
    pet_species_entry.pack(pady=5)

    ctk.CTkLabel(input_frame, text="Tuổi:", font=("Arial", 12)).pack(pady=5, anchor="w")
    pet_age_entry = ctk.CTkEntry(input_frame, width=250)
    pet_age_entry.pack(pady=5)

    ctk.CTkLabel(input_frame, text="Giới tính:", font=("Arial", 12)).pack(pady=5, anchor="w")
    pet_gender_entry = ctk.CTkComboBox(input_frame, values=["Male", "Female"], width=250)
    pet_gender_entry.pack(pady=5)

    ctk.CTkLabel(input_frame, text="ID chủ vật nuôi:", font=("Arial", 12)).pack(pady=5, anchor="w")
    owner_id_entry = ctk.CTkEntry(input_frame, width=250)
    owner_id_entry.pack(pady=5)

    # Frame bên phải: Chứa bảng và nút chức năng
    right_frame = ctk.CTkFrame(content_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

    # Frame cho bảng hiển thị danh sách thú cưng
    table_frame = ctk.CTkFrame(right_frame)
    table_frame.pack(fill="both", expand=True, pady=5)

    # Tạo bảng với Treeview
    columns = ("id", "ten", "loai", "tuoi", "gioi_tinh", "id_chu_so_huu")
    tree = Treeview(table_frame, columns=columns, show="headings", height=15)
    tree.heading("id", text="ID")
    tree.heading("ten", text="Tên")
    tree.heading("loai", text="Loài")
    tree.heading("tuoi", text="Tuổi")
    tree.heading("gioi_tinh", text="Giới tính")
    tree.heading("id_chu_so_huu", text="ID Chủ")

    # Đặt chiều rộng cho các cột
    tree.column("id", width=80)
    tree.column("ten", width=150)
    tree.column("loai", width=150)
    tree.column("tuoi", width=80)
    tree.column("gioi_tinh", width=100)
    tree.column("id_chu_so_huu", width=120)
    tree.pack(fill="both", expand=True)

    # Frame cho các nút chức năng (dưới bảng)
    button_frame = ctk.CTkFrame(right_frame)
    button_frame.pack(fill="x", padx=10, pady=5)

    # Sắp xếp các nút nằm ngang dưới bảng
    add_button = ctk.CTkButton(button_frame, text="Add Pet", command=lambda: add_pet_handler(pet_controller_instance), width=120)
    add_button.pack(side="left", padx=5)

    update_button = ctk.CTkButton(button_frame, text="Update Pet", command=lambda: update_pet_handler(pet_controller_instance), width=120)
    update_button.pack(side="left", padx=5)

    delete_button = ctk.CTkButton(button_frame, text="Delete Pet", command=lambda: delete_pet_handler(pet_controller_instance), width=120)
    delete_button.pack(side="left", padx=5)

    search_button = ctk.CTkButton(button_frame, text="Search", command=lambda: search_pet_handler(pet_controller_instance), width=120)
    search_button.pack(side="left", padx=5)

    delete_all_button = ctk.CTkButton(button_frame, text="Delete All", command=lambda: delete_all_handler(pet_controller_instance), width=120)
    delete_all_button.pack(side="left", padx=5)

    # Hàm tải danh sách thú cưng
    def load_pets(pets=None):
        for item in tree.get_children():
            tree.delete(item)
        if pets is None:
            pets = pet_controller_instance.get_all_pets()
        for pet in pets:
            tree.insert("", "end", values=pet)

    # Hàm xử lý khi chọn một dòng trong bảng
    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item[0])["values"]
            pet_id_entry.delete(0, ctk.END)
            pet_name_entry.delete(0, ctk.END)
            pet_species_entry.delete(0, ctk.END)
            pet_age_entry.delete(0, ctk.END)
            pet_gender_entry.set("")
            owner_id_entry.delete(0, ctk.END)

            pet_id_entry.insert(0, item[0])
            pet_name_entry.insert(0, item[1])
            pet_species_entry.insert(0, item[2])
            pet_age_entry.insert(0, item[3])
            pet_gender_entry.set(item[4])
            owner_id_entry.insert(0, item[5])

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # Hàm thêm thú cưng
    def add_pet_handler(controller):
        pet_data = {
            "ID vật nuôi": pet_id_entry.get(),
            "Tên vật nuôi": pet_name_entry.get(),
            "Loài": pet_species_entry.get(),
            "Tuổi": pet_age_entry.get(),
            "Giới tính": pet_gender_entry.get(),
            "ID chủ vật nuôi": owner_id_entry.get()
        }
        controller.add_pet(pet_data)
        load_pets()
        clear_form()

    # Hàm xóa thú cưng
    def delete_pet_handler(controller):
        pet_id = pet_id_entry.get()
        controller.delete_pet(pet_id)
        load_pets()
        clear_form()

    # Hàm sửa thú cưng
    def update_pet_handler(controller):
        pet_data = {
            "ID vật nuôi": pet_id_entry.get(),
            "Tên vật nuôi": pet_name_entry.get(),
            "Loài": pet_species_entry.get(),
            "Tuổi": pet_age_entry.get(),
            "Giới tính": pet_gender_entry.get(),
            "ID chủ vật nuôi": owner_id_entry.get()
        }
        controller.update_pet(pet_data)
        load_pets()
        clear_form()

    # Hàm tìm kiếm
    def search_pet_handler(controller):
        keyword = pet_id_entry.get()
        field = "id"
        pets = controller.search_pets(keyword, field)
        if pets:
            load_pets(pets)

    # Hàm xóa tất cả
    def delete_all_handler(controller):
        controller.delete_all_pets()
        load_pets()
        clear_form()

    # Hàm xóa nội dung form
    def clear_form():
        pet_id_entry.delete(0, ctk.END)
        pet_name_entry.delete(0, ctk.END)
        pet_species_entry.delete(0, ctk.END)
        pet_age_entry.delete(0, ctk.END)
        pet_gender_entry.set("")
        owner_id_entry.delete(0, ctk.END)

    # Nút quay lại
    back_button = ctk.CTkButton(frame, text="Quay lại", command=lambda: __import__('views.main_view').set_content(__import__('views.main_view').show_home_content))
    back_button.pack(pady=10)

    load_pets()