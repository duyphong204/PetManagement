import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview, Style
import controllers.quanlythuoc_controller as drug_controller

def open_manage_drug_content(frame):
    # Khởi tạo Controller
    drug_controller_instance = drug_controller.DrugController()

    # Tiêu đề
    title_label = ctk.CTkLabel(frame, text="Quản lý Thuốc", font=("Arial", 18, "bold"), text_color="black")
    title_label.pack(pady=10)

    # Frame chính chứa toàn bộ nội dung
    content_frame = ctk.CTkFrame(frame)
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Frame bên trái: Ô nhập liệu
    input_frame = ctk.CTkFrame(content_frame, width=200)
    input_frame.pack(side="left", padx=10, pady=5, fill="y")

    # Các ô nhập liệu
    entries = {}
    fields = ["Tên thuốc", "Mô tả", "Đơn vị", "Giá", "Hạn sử dụng", "Số lượng"]
    for field in fields:
        ctk.CTkLabel(input_frame, text=f"{field}:", font=("Arial", 12)).pack(pady=5, anchor="w")
        if field == "Đơn vị":
            entry = ctk.CTkComboBox(input_frame, values=["Viên", "Chai", "Gói", "Ống"], width=250)
        else:
            entry = ctk.CTkEntry(input_frame, width=250)
        entry.pack(pady=5)
        entries[field] = entry

    # Frame bên phải: Chứa bảng và nút chức năng
    right_frame = ctk.CTkFrame(content_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

    # Frame cho tìm kiếm
    search_frame = ctk.CTkFrame(right_frame)
    search_frame.pack(fill="x", pady=5)
    ctk.CTkLabel(search_frame, text="Tìm kiếm:", font=("Arial", 12)).pack(side="left", padx=5)
    search_entry = ctk.CTkEntry(search_frame, width=200)
    search_entry.pack(side="left", padx=5)

    # Frame cho bảng
    table_frame = ctk.CTkFrame(right_frame)
    table_frame.pack(fill="both", expand=True, pady=5)

    # Tạo và cấu hình Style cho Treeview
    style = Style()
    style.configure("Treeview.Heading", font=("Arial", 16, "bold"))
    style.configure("Treeview", font=("Arial", 14))

    # Tạo bảng với Treeview
    columns = ("id", "ten_thuoc", "mo_ta", "don_vi", "gia", "han_su_dung", "so_luong")
    tree = Treeview(table_frame, columns=columns, show="headings", height=15, style="Treeview")
    for col, text in zip(columns, ["ID", "Tên Thuốc", "Mô Tả", "Đơn Vị", "Giá", "Hạn Sử Dụng", "Số Lượng"]):
        tree.heading(col, text=text)
    tree.column("id", width=50)
    tree.column("ten_thuoc", width=150)
    tree.column("mo_ta", width=200)
    tree.column("don_vi", width=50)
    tree.column("gia", width=50)
    tree.column("han_su_dung", width=150)
    tree.column("so_luong", width=50)
    tree.pack(fill="both", expand=True)

    # Frame cho các nút chức năng
    button_frame = ctk.CTkFrame(right_frame)
    button_frame.pack(fill="x", padx=10, pady=5)

    # Hàm hiển thị dữ liệu lên bảng
    def display_drugs(drugs):
        for item in tree.get_children():
            tree.delete(item)
        if drugs:
            for drug in drugs:
                if len(drug) == 7:
                    tree.insert("", "end", values=drug)
        else:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị.")

    # Hàm xóa nội dung form
    def clear_form():
        for field, entry in entries.items():
            if isinstance(entry, ctk.CTkComboBox):
                entry.set("")  
            else:
                entry.delete(0, ctk.END)

    # Hàm xử lý khi chọn một dòng trong bảng
    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item[0])["values"]
            for i, (field, entry) in enumerate(entries.items(), start=1):
                value = item[i] if item[i] is not None else ""
                if isinstance(entry, ctk.CTkComboBox):
                    entry.set(value)  # Chỉ dùng set() cho CTkComboBox
                else:
                    entry.delete(0, ctk.END)  # Chỉ dùng delete + insert cho CTkEntry
                    entry.insert(0, value)

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # Hàm tìm kiếm
    def search():
        keyword = search_entry.get().strip() 
        drugs = drug_controller_instance.search_drugs(keyword)
        display_drugs(drugs)
        if not drugs and keyword:
            messagebox.showinfo("Thông báo", "Không tìm thấy thuốc.")

    # Hàm xử lý chung cho các thao tác (Add, Update, Delete)
    def handle_action(action, success_message):
        try:
            drug_data = {field: entry.get() for field, entry in entries.items()}
            
            # Kiểm tra dữ liệu đầu vào
            if action in ["add", "update"]:
                for field, value in drug_data.items():
                    if not value:
                        messagebox.showwarning("Cảnh báo", f"Vui lòng nhập {field} để {action == 'add' and 'thêm' or 'cập nhật'} thuốc.")
                        return
            elif action == "delete":
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn thuốc để xóa!")
                    return
                drug_id = tree.item(selected_item[0])["values"][0]

            # Thực hiện hành động
            if action == "add":
                if drug_controller_instance.add_drug(drug_data):
                    messagebox.showinfo("Thành công", success_message)
            elif action == "update":
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn thuốc để cập nhật!")
                    return
                drug_id = tree.item(selected_item[0])["values"][0]
                if drug_controller_instance.update_drug(drug_id, drug_data):
                    messagebox.showinfo("Thành công", success_message)
            elif action == "delete":
                confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa thuốc này không?")
                if confirm and drug_controller_instance.delete_drug(drug_id):
                    messagebox.showinfo("Thành công", success_message)

            # Tải lại bảng sau khi thực hiện hành động
            drugs = drug_controller_instance.get_all_drugs()
            display_drugs(drugs)
            clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi {action == 'add' and 'thêm' or action == 'update' and 'cập nhật' or action == 'delete' and 'xóa'} thuốc: {e}")

    # Các nút chức năng
    ctk.CTkButton(search_frame, text="Tìm", command=search, width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Add Drug", command=lambda: handle_action("add", "Thêm thuốc thành công!"), width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Update Drug", command=lambda: handle_action("update", "Cập nhật thuốc thành công!"), width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Delete Drug", command=lambda: handle_action("delete", "Xóa thuốc thành công!"), width=120).pack(side="left", padx=5)

    # Tải dữ liệu ban đầu
    try:
        drugs = drug_controller_instance.get_all_drugs()
        display_drugs(drugs)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu ban đầu: {e}")
