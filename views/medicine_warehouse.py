import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview
from tkcalendar import DateEntry
import controllers.medicine_warehouse_controller as medicine_controller

def open_manage_medicine_content(frame):
    medicine_controller_instance = medicine_controller.ManageMedicineWarehouseController()

    def clear_form():
        medicine_name_entry.delete(0, ctk.END)
        quantity_entry.delete(0, ctk.END)
        import_date_entry.delete(0, ctk.END)
        expiry_date_entry.delete(0, ctk.END)

    def load_medicines(medicines=None):
        for item in tree.get_children():
            tree.delete(item)
        if medicines is None:
            medicines = medicine_controller_instance.get_all_medicines()
        for medicine in medicines:
            tree.insert("", "end", values=medicine)
    
    def add_medicine_handler():
        medicine_data = {
            "Tên thuốc": medicine_name_entry.get(),
            "Số lượng": quantity_entry.get(),
            "Ngày nhập": import_date_entry.get(),
            "Hạn sử dụng": expiry_date_entry.get()
        }
        medicine_controller_instance.add_medicine(medicine_data)
        load_medicines()
        clear_form()

    def delete_medicine_handler():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thuốc để xóa!")
            return
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa thuốc này không?")
        if not confirm:
            return
        medicine_id = tree.item(selected_item[0])["values"][0]
        medicine_controller_instance.delete_medicine(medicine_id)
        load_medicines()
        clear_form()

    def update_medicine_handler():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thuốc để cập nhật!")
            return
        medicine_id = tree.item(selected_item[0])["values"][0]
        medicine_data = {
            "ID": medicine_id,
            "Tên thuốc": medicine_name_entry.get(),
            "Số lượng": quantity_entry.get(),
            "Ngày nhập": import_date_entry.get(),
            "Hạn sử dụng": expiry_date_entry.get()
        }
        medicine_controller_instance.update_medicine(medicine_data)
        load_medicines()
        clear_form()

    def search_medicine_handler():
        keyword = search_entry.get().strip()
        field = search_field.get()
        if not keyword or not field:
            load_medicines()
            return
        medicines = medicine_controller_instance.search_medicines(keyword, field)
        load_medicines(medicines)

    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item[0])["values"]
            medicine_name_entry.delete(0, ctk.END)
            medicine_name_entry.insert(0, item[1])

            quantity_entry.delete(0, ctk.END)
            quantity_entry.insert(0, item[2])

            import_date_entry.delete(0, ctk.END)
            import_date_entry.insert(0, item[3])

            expiry_date_entry.delete(0, ctk.END)
            expiry_date_entry.insert(0, item[4])

    title_label = ctk.CTkLabel(frame, text="Quản lý Kho Thuốc", font=("Arial", 18, "bold"), text_color="black")
    title_label.pack(pady=10)

    content_frame = ctk.CTkFrame(frame)
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    input_frame = ctk.CTkFrame(content_frame, width=300)
    input_frame.pack(side="left", padx=10, pady=5, fill="y")

    medicine_name_entry = ctk.CTkEntry(input_frame, width=250)
    quantity_entry = ctk.CTkEntry(input_frame, width=250)
    import_date_entry = DateEntry(input_frame, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    expiry_date_entry = DateEntry(input_frame, width=20, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')

    for label, entry in [
        ("Tên thuốc:", medicine_name_entry),
        ("Số lượng:", quantity_entry),
        ("Ngày nhập:", import_date_entry),
        ("Hạn sử dụng:", expiry_date_entry),
    ]:
        ctk.CTkLabel(input_frame, text=label, font=("Arial", 12)).pack(pady=5, anchor="w")
        entry.pack(pady=5)

    right_frame = ctk.CTkFrame(content_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

    search_frame = ctk.CTkFrame(right_frame)
    search_frame.pack(fill="x", pady=5, padx=10)

    ctk.CTkLabel(search_frame, text="Tìm kiếm:", font=("Arial", 12)).pack(side="left", padx=5)
    search_entry = ctk.CTkEntry(search_frame, width=200, placeholder_text="Nhập từ khóa tìm kiếm...")
    search_entry.pack(side="left", padx=5)

    search_field = ctk.CTkComboBox(search_frame, values=["Tên thuốc", "Số lượng", "Ngày nhập", "Hạn sử dụng"], width=150)
    search_field.pack(side="left", padx=5)

    table_frame = ctk.CTkFrame(right_frame)
    table_frame.pack(fill="both", expand=True, pady=5)

    columns = ("id", "ten_thuoc", "so_luong", "ngay_nhap", "han_su_dung")
    tree = Treeview(table_frame, columns=columns, show="headings", height=15)

    for col, text, width in [
        ("id", "ID", 30),
        ("ten_thuoc", "Tên thuốc", 150),
        ("so_luong", "Số lượng", 100),
        ("ngay_nhap", "Ngày nhập", 120),
        ("han_su_dung", "Hạn sử dụng", 120),
    ]:
        tree.heading(col, text=text)
        tree.column(col, width=width)

    tree.pack(fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    button_frame = ctk.CTkFrame(right_frame)
    button_frame.pack(fill="x", padx=10, pady=5)

    add_button = ctk.CTkButton(button_frame, text="Thêm thuốc", command=add_medicine_handler, width=120)
    add_button.pack(side="left", padx=5)

    update_button = ctk.CTkButton(button_frame, text="Sửa thuốc", command=update_medicine_handler, width=120)
    update_button.pack(side="left", padx=5)

    delete_button = ctk.CTkButton(button_frame, text="Xóa thuốc", command=delete_medicine_handler, width=120)
    delete_button.pack(side="left", padx=5)

    search_button = ctk.CTkButton(button_frame, text="Tìm kiếm", command=search_medicine_handler)
    search_button.pack(side="left", padx=5)

    load_medicines()