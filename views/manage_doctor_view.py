import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview, Style
import controllers.quanlybacsi_controller as doctor_controller

def open_manage_doctor_content(frame):
   
    doctor_controller_instance = doctor_controller.DoctorController()

    
    title_label = ctk.CTkLabel(frame, text="Quản lý Bác sĩ", font=("Arial", 18, "bold"), text_color="black")
    title_label.pack(pady=10)

    # Frame chính chứa nội dung
    content_frame = ctk.CTkFrame(frame)
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Frame bên trái: Ô nhập liệu
    input_frame = ctk.CTkFrame(content_frame, width=200)
    input_frame.pack(side="left", padx=10, pady=5, fill="y")

    # Các ô nhập liệu
    entries = {}
    fields = ["Họ tên", "Chuyên môn", "Số điện thoại", "Email", "ID Người Dùng"]
    
    for field in fields:
        ctk.CTkLabel(input_frame, text=f"{field}:", font=("Arial", 12)).pack(pady=5, anchor="w")
        
        if field == "ID Người Dùng":
          
            entry = ctk.CTkEntry(input_frame, width=250, validate="key", validatecommand=(frame.register(validate_id), "%P"))
        else:
            entry = ctk.CTkEntry(input_frame, width=250)
        
        entry.pack(pady=5)
        entries[field] = entry

    # Frame bên phải: Chứa bảng và nút chức năng
    right_frame = ctk.CTkFrame(content_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

    # Frame tìm kiếm
    search_frame = ctk.CTkFrame(right_frame)
    search_frame.pack(fill="x", pady=5)
    ctk.CTkLabel(search_frame, text="Tìm kiếm:", font=("Arial", 12)).pack(side="left", padx=5)
    search_entry = ctk.CTkEntry(search_frame, width=200)
    search_entry.pack(side="left", padx=5)

    # Frame bảng
    table_frame = ctk.CTkFrame(right_frame)
    table_frame.pack(fill="both", expand=True, pady=5)

    # Tạo Style cho Treeview
    style = Style()
    style.configure("Treeview.Heading", font=("Arial", 16, "bold"))
    style.configure("Treeview", font=("Arial", 14))

    # Tạo bảng Treeview
    columns = ("id", "ho_ten", "chuyen_mon", "so_dien_thoai", "email", "id_nguoi_dung")
    tree = Treeview(table_frame, columns=columns, show="headings", height=15, style="Treeview")
    
    for col, text in zip(columns, ["ID", "Họ tên", "Chuyên môn", "Số điện thoại", "Email", "ID Người dùng"]):
        tree.heading(col, text=text)

    tree.column("id", width=80)
    tree.column("ho_ten", width=200)
    tree.column("chuyen_mon", width=200)
    tree.column("so_dien_thoai", width=150)
    tree.column("email", width=200)
    tree.column("id_nguoi_dung", width=120)

    tree.pack(fill="both", expand=True)

    # Frame nút chức năng
    button_frame = ctk.CTkFrame(right_frame)
    button_frame.pack(fill="x", padx=10, pady=5)

    # Hiển thị dữ liệu lên bảng
    def display_doctors(doctors):
        for item in tree.get_children():
            tree.delete(item)
        if doctors:
            for doctor in doctors:
                if len(doctor) == 6:
                    tree.insert("", "end", values=doctor)
        else:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị.")

    # Xóa nội dung form
    def clear_form():
        for entry in entries.values():
            entry.delete(0, ctk.END)

    # Chọn một dòng trong bảng
    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item[0])["values"]
            for i, (field, entry) in enumerate(entries.items(), start=1):
                entry.delete(0, ctk.END)
                entry.insert(0, item[i] if item[i] else "")

    tree.bind("<<TreeviewSelect>>", on_tree_select)

   
    def search():
        keyword = search_entry.get().strip()
        doctors = doctor_controller_instance.search_doctors(keyword)
        display_doctors(doctors)
        if not doctors and keyword:
            messagebox.showinfo("Thông báo", "Không tìm thấy bác sĩ.")

    # Xử lý các thao tác (Add, Update, Delete)
    def handle_action(action, success_message):
        try:
       
            doctor_data = {field: entry.get() for field, entry in entries.items()}
      
            if action in ["add", "update"]:
                for field, value in doctor_data.items():
                    if not value and field != "ID Người Dùng":
                        messagebox.showwarning("Cảnh báo", f"Vui lòng nhập {field}.")
                        return


            # Tự động điền số "0" ở đầu nếu chưa có cho số điện thoại
                phone_number = doctor_data.get("Số điện thoại")
                if phone_number and not phone_number.startswith("0"):
                    doctor_data["Số điện thoại"] = "0" + phone_number

        # Thực hiện hành động (add, update, delete)
            if action == "add":
                if doctor_controller_instance.add_doctor(doctor_data):
                    messagebox.showinfo("Thành công", success_message)
            elif action == "update":
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn bác sĩ để cập nhật!")
                    return
                doctor_id = tree.item(selected_item[0])["values"][0]
                if doctor_controller_instance.update_doctor(doctor_id, doctor_data):
                    messagebox.showinfo("Thành công", success_message)
            elif action == "delete":
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn bác sĩ để xóa!")
                    return
                doctor_id = tree.item(selected_item[0])["values"][0]
                confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa bác sĩ này không?")
                if confirm and doctor_controller_instance.delete_doctor(doctor_id):
                    messagebox.showinfo("Thành công", success_message)

        # Cập nhật lại bảng sau khi thực hiện hành động
            doctors = doctor_controller_instance.get_all_doctors()
            display_doctors(doctors)
            clear_form() 
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi {action}: {e}")

    
    ctk.CTkButton(search_frame, text="Tìm", command=search, width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Thêm bác sĩ", command=lambda: handle_action("add", "Thêm bác sĩ thành công!"), width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Cập nhật bác sĩ", command=lambda: handle_action("update", "Cập nhật bác sĩ thành công!"), width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Xóa bác sĩ", command=lambda: handle_action("delete", "Xóa bác sĩ thành công!"), width=120).pack(side="left", padx=5)

    
    try:
        doctors = doctor_controller_instance.get_all_doctors()
        display_doctors(doctors)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu ban đầu: {e}")

def validate_id(value):
    """ Kiểm tra xem giá trị nhập vào có phải là số nguyên hợp lệ không. """
    if value == "" or value.isdigit():
        return True
    return False