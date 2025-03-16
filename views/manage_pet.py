import customtkinter as ctk
from models.manage_pet_model import PetModel
from tkinter import messagebox
from tkinter.ttk import Treeview, Style
import controllers.manage_pet_controller as pet_controller

def open_manage_pet_content(frame):
    # Khởi tạo Controller
    pet_controller_instance = pet_controller.ManagePetController()

    # Tiêu đề
    title_label = ctk.CTkLabel(frame, text="Quản lý Thú cưng", font=("Arial", 18, "bold"), text_color="black")
    title_label.pack(pady=10)

    # Frame chính chứa toàn bộ nội dung
    content_frame = ctk.CTkFrame(frame)
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Frame bên trái: Ô nhập liệu
    input_frame = ctk.CTkFrame(content_frame, width=200)
    input_frame.pack(side="left", padx=10, pady=5, fill="y")

    # Các ô nhập liệu
    entries = {}
    fields = ["ID vật nuôi", "Tên vật nuôi", "Loài", "Tuổi", "Giới tính", "ID chủ vật nuôi"]
    for field in fields:
        ctk.CTkLabel(input_frame, text=f"{field}:", font=("Arial", 12)).pack(pady=5, anchor="w")
        if field == "Giới tính":
            entry = ctk.CTkComboBox(input_frame, values=["Male", "Female"], width=250)
        else:
            entry = ctk.CTkEntry(input_frame, width=250)
        entry.pack(pady=5)
        entries[field] = entry

    # Frame bên phải: Chứa bảng và nút chức năng
    right_frame = ctk.CTkFrame(content_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

    # Frame cho bảng
    table_frame = ctk.CTkFrame(right_frame)
    table_frame.pack(fill="both", expand=True, pady=5)

    # Tạo và cấu hình Style cho Treeview
    style = Style()
    style.configure("Treeview.Heading", font=("Arial", 16, "bold"))
    style.configure("Treeview", font=("Arial", 14))

    # Tạo bảng với Treeview
    columns = ("id", "ten", "loai", "tuoi", "gioi_tinh", "id_chu_so_huu")
    tree = Treeview(table_frame, columns=columns, show="headings", height=15, style="Treeview")
    for col, text in zip(columns, ["ID", "Tên", "Loài", "Tuổi", "Giới tính", "ID Chủ"]):
        tree.heading(col, text=text)
    tree.column("id", width=120)
    tree.column("ten", width=200)
    tree.column("loai", width=200)
    tree.column("tuoi", width=120)
    tree.column("gioi_tinh", width=140)
    tree.column("id_chu_so_huu", width=160)
    tree.pack(fill="both", expand=True)

    # Frame cho các nút chức năng
    button_frame = ctk.CTkFrame(right_frame)
    button_frame.pack(fill="x", padx=10, pady=5)

    # Hàm hiển thị dữ liệu lên bảng
    def display_pets(pets):
        for item in tree.get_children():
            tree.delete(item)
        if pets:
            for pet in pets:
                if len(pet) == 6:
                    tree.insert("", "end", values=pet)
        else:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị.")

    # Hàm xóa nội dung form
    def clear_form():
        for field, entry in entries.items():
            if field == "Giới tính":
                entry.set("")
            else:
                entry.delete(0, ctk.END)

    # Hàm xử lý khi chọn một dòng trong bảng
    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item[0])["values"]
            for i, (field, entry) in enumerate(entries.items()):
                if field == "Giới tính":
                    entry.set(item[i] if item[i] else "")
                else:
                    entry.delete(0, ctk.END)
                    entry.insert(0, item[i] if item[i] else "")

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # Hàm xử lý chung cho các thao tác (Add, Update, Delete, Search)
    def handle_action(action, success_message):
        try:
            pet_data = {field: entry.get() for field, entry in entries.items()}
            
            # Kiểm tra dữ liệu đầu vào
            if action in ["add", "update"]:
                # Kiểm tra tất cả các trường không được để trống
                for field, value in pet_data.items():
                    if not value:
                        messagebox.showwarning("Cảnh báo", f"Vui lòng nhập {field} để {action == 'add' and 'thêm' or 'cập nhật'} thú cưng.")
                        return
            elif action in ["delete", "search"]:
                # Chỉ kiểm tra ID không được để trống
                pet_id = pet_data["ID vật nuôi"]
                if not pet_id:
                    messagebox.showwarning("Cảnh báo", f"Vui lòng nhập ID thú cưng để {action == 'delete' and 'xóa' or 'tìm kiếm'}.")
                    return

            # Thực hiện hành động
            if action == "add":
                pet_controller_instance.add_pet(pet_data)
            elif action == "update":
                pet_controller_instance.update_pet(pet_data)
            elif action == "delete":
                pet_controller_instance.delete_pet(pet_data["ID vật nuôi"])
            elif action == "search":
                pets = pet_controller_instance.search_pets(pet_data["ID vật nuôi"], "id")
                display_pets(pets)
                if not pets:
                    messagebox.showinfo("Thông báo", "Không tìm thấy thú cưng.")
                return

            # Tải lại bảng sau khi thực hiện hành động
            pets = pet_controller_instance.get_all_pets()
            display_pets(pets)
            clear_form()
            messagebox.showinfo("Thành công", success_message)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi {action == 'add' and 'thêm' or action == 'update' and 'cập nhật' or action == 'delete' and 'xóa' or 'tìm kiếm'} thú cưng: {e}")

    # Các nút chức năng
    ctk.CTkButton(button_frame, text="Add Pet", command=lambda: handle_action("add", "Thêm thú cưng thành công!"), width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Update Pet", command=lambda: handle_action("update", "Cập nhật thú cưng thành công!"), width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Delete Pet", command=lambda: handle_action("delete", "Xóa thú cưng thành công!"), width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Search", command=lambda: handle_action("search", ""), width=120).pack(side="left", padx=5)

    # Tải dữ liệu ban đầu
    try:
        pets = pet_controller_instance.get_all_pets()
        display_pets(pets)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu ban đầu: {e}")