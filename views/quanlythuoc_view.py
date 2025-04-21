import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkcalendar import DateEntry
import controllers.quanlythuoc_controller as drug_controller

def open_manage_drug_content(frame):
    # Khởi tạo Controller
    drug_controller_instance = drug_controller.DrugController()

    # Xóa nội dung các ô nhập liệu
    def clear_form():
        for field, entry in entries.items():
            if isinstance(entry, ctk.CTkComboBox):
                entry.set("")
            else:
                entry.delete(0, ctk.END)

    # Tạo danh sách thuốc vào bảng treeview
    def load_drugs(drugs=None):
        for item in tree.get_children():
            tree.delete(item)
        if drugs is None:
            drugs = drug_controller_instance.get_all_drugs()
        for drug in drugs:
            tree.insert("", "end", values=drug)

    # Xử lý thêm thuốc mới
    def add_drug_handler():
        drug_data = {field: entry.get() for field, entry in entries.items()}
        drug_controller_instance.add_drug(drug_data)
        load_drugs()
        clear_form()

    # Xử lý xóa thuốc
    def delete_drug_handler():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thuốc để xóa!")
            return
        drug_id = tree.item(selected_item[0])["values"][0]
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa thuốc này không?")
        if confirm:
            drug_controller_instance.delete_drug(drug_id)
            load_drugs()
            clear_form()

    # Xử lý cập nhật thuốc
    def update_drug_handler():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thuốc để cập nhật!")
            return
        drug_id = tree.item(selected_item[0])["values"][0]
        drug_data = {field: entry.get() for field, entry in entries.items()}
        drug_controller_instance.update_drug(drug_id, drug_data)
        load_drugs()
        clear_form()

    # Xử lý tìm kiếm
    def search_drug_handler():
        keyword = search_entry.get().strip()
        field = search_field.get()
        if not keyword or not field:
            load_drugs()
            return
        drugs = drug_controller_instance.search_drugs(keyword, field)
        load_drugs(drugs)

    # Xử lý sự kiện khi người dùng chọn một dòng trong bảng
    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item[0])["values"]
            for i, (field, entry) in enumerate(entries.items()):
                value = item[i + 1] if (i + 1) < len(item) else ""
                if isinstance(entry, ctk.CTkComboBox):
                    entry.set(value)
                else:
                    entry.delete(0, ctk.END)
                    entry.insert(0, value)

    # Tiêu đề
    title_label = ctk.CTkLabel(frame, text="Quản lý Thuốc", font=("Arial", 18, "bold"))
    title_label.pack(pady=10)

    # Form nhập thông tin thuốc
    content_frame = ctk.CTkFrame(frame)
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    input_frame = ctk.CTkFrame(content_frame, width=300)
    input_frame.pack(side="left", padx=10, pady=5, fill="y")

    # Các ô nhập liệu
    entries = {}
    fields = ["Tên thuốc", "Loại thuốc", "Nhà sản xuất", "Giá"]
    for field in fields:
        ctk.CTkLabel(input_frame, text=f"{field}:", font=("Arial", 12)).pack(pady=5, anchor="w")
        if field == "Loại thuốc":
            entry = ctk.CTkComboBox(input_frame, values=["Vắc-xin", "Kháng sinh", "Bổ sung", "Khác"], width=250)
        else:
            entry = ctk.CTkEntry(input_frame, width=250)
        entry.pack(pady=5)
        entries[field] = entry

    # Frame bên phải: Chứa bảng và nút chức năng
    right_frame = ctk.CTkFrame(content_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

    # Ô tìm kiếm
    search_frame = ctk.CTkFrame(right_frame)
    search_frame.pack(fill="x", pady=5, padx=10)

    # Ô tìm kiếm từ khóa
    ctk.CTkLabel(search_frame, text="Tìm kiếm:", font=("Arial", 12)).pack(side="left", padx=5)
    search_entry = ctk.CTkEntry(search_frame, width=200, placeholder_text="Nhập từ khóa tìm kiếm...")
    search_entry.pack(side="left", padx=5)

    # Combobox chọn trường tìm kiếm
    search_field = ctk.CTkComboBox(search_frame, values=["Tên thuốc", "Loại thuốc", "Nhà sản xuất", "Giá"], width=150)
    search_field.pack(side="left", padx=5)

    # Hiển thị danh sách thuốc trong bảng
    table_frame = ctk.CTkFrame(right_frame)
    table_frame.pack(fill="both", expand=True, pady=5)

    columns = ("id", "ten_thuoc", "loai_thuoc", "nha_san_xuat", "gia")
    tree = Treeview(table_frame, columns=columns, show="headings", height=15)

    for col, text, width in [
        ("id", "ID", 30),
        ("ten_thuoc", "Tên thuốc", 150),
        ("loai_thuoc", "Loại thuốc", 100),
        ("nha_san_xuat", "Nhà sản xuất", 150),
        ("gia", "Giá", 100),
    ]:
        tree.heading(col, text=text)
        tree.column(col, width=width)

    tree.pack(fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # Frame cho các nút chức năng
    button_frame = ctk.CTkFrame(right_frame)
    button_frame.pack(fill="x", padx=10, pady=5)

    # Các nút điều khiển
    add_button = ctk.CTkButton(button_frame, text="Add Drug", command=add_drug_handler, width=120)
    add_button.pack(side="left", padx=5)

    update_button = ctk.CTkButton(button_frame, text="Update Drug", command=update_drug_handler, width=120)
    update_button.pack(side="left", padx=5)

    delete_button = ctk.CTkButton(button_frame, text="Delete Drug", command=delete_drug_handler, width=120)
    delete_button.pack(side="left", padx=5)

    search_button = ctk.CTkButton(button_frame, text="Search", command=search_drug_handler, width=120)
    search_button.pack(side="left", padx=5)

    load_drugs()