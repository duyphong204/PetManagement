import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview
import controllers.KeDon_controller as prescription_controller

def open_manage_prescription_content(frame):
    # Khởi tạo Controller
    prescription_controller_instance = prescription_controller.PrescriptionController()

    # Lấy danh sách lịch hẹn
    appointments = prescription_controller_instance.get_appointments()
    appointment_display = [f"ID: {appt[0]} - {appt[1]} (BS: {appt[2]}) - {appt[3]} {appt[4]}" for appt in appointments]
    appointment_dict = {f"ID: {appt[0]} - {appt[1]} (BS: {appt[2]}) - {appt[3]} {appt[4]}": appt[0] for appt in appointments}

    # Lấy danh sách thuốc kèm số lượng
    medicines = prescription_controller_instance.get_medicines()
    medicine_display = [f"{medicine[1]} (Số lượng: {medicine[2] if medicine[2] is not None else 0})" for medicine in medicines]
    medicine_dict = {f"{medicine[1]} (Số lượng: {medicine[2] if medicine[2] is not None else 0})": medicine[1] for medicine in medicines}
    medicine_quantity_dict = {medicine[1]: medicine[2] if medicine[2] is not None else 0 for medicine in medicines}

    # Xóa nội dung các ô nhập liệu
    def clear_form():
        appointment_entry.set("")
        medicine_entry.set("")
        quantity_entry.delete(0, ctk.END)
        duration_entry.delete(0, ctk.END)
        instruction_entry.delete(0, ctk.END)

    # Tạo danh sách đơn thuốc vào bảng treeview
    def load_prescriptions(prescriptions=None):
        for item in tree.get_children():
            tree.delete(item)
        if prescriptions is None:
            prescriptions = prescription_controller_instance.get_all_prescriptions()
        for prescription in prescriptions:
            tree.insert("", "end", values=prescription)

    # Kiểm tra số lượng thuốc khi nhập
    def check_quantity(*args):
        selected_medicine = medicine_dict.get(medicine_entry.get())
        if not selected_medicine:
            return
        try:
            quantity = int(quantity_entry.get())
            available_quantity = medicine_quantity_dict.get(selected_medicine, 0)
            if quantity > available_quantity:
                messagebox.showwarning("Cảnh báo", f"Số lượng trong kho không đủ! Hiện có: {available_quantity}")
                quantity_entry.delete(0, ctk.END)
                quantity_entry.insert(0, str(available_quantity))
        except ValueError:
            pass  # Ignore if quantity is not a number yet

    # Xử lý kê đơn
    def prescribe_handler():
        ten_thuoc = medicine_dict.get(medicine_entry.get())
        if not ten_thuoc:
            messagebox.showerror("Lỗi", "Vui lòng chọn thuốc!")
            return

        prescription_data = {
            "ID Lịch hẹn": appointment_dict.get(appointment_entry.get()),
            "Tên thuốc": ten_thuoc,
            "Số lượng": quantity_entry.get(),
            "Thời gian sử dụng": duration_entry.get(),
            "Hướng dẫn": instruction_entry.get()
        }
        if prescription_controller_instance.prescribe_medicine(prescription_data):
            # Cập nhật số lượng trong Combobox
            available_quantity = medicine_quantity_dict[ten_thuoc] - int(quantity_entry.get())
            medicine_quantity_dict[ten_thuoc] = available_quantity
            new_display = [f"{name.split(' (')[0]} (Số lượng: {medicine_quantity_dict[name.split(' (')[0]]})" for name in medicine_display]
            medicine_entry.configure(values=new_display)
            load_prescriptions()
            clear_form()

    # Xử lý sửa đơn thuốc
    def edit_prescription_handler():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn đơn thuốc để sửa!")
            return
        prescription_id = tree.item(selected_item[0])["values"][0]

        ten_thuoc = medicine_dict.get(medicine_entry.get())
        if not ten_thuoc:
            messagebox.showerror("Lỗi", "Vui lòng chọn thuốc!")
            return

        prescription_data = {
            "ID Lịch hẹn": appointment_dict.get(appointment_entry.get()),
            "Tên thuốc": ten_thuoc,
            "Số lượng": quantity_entry.get(),
            "Thời gian sử dụng": duration_entry.get(),
            "Hướng dẫn": instruction_entry.get()
        }
        if prescription_controller_instance.update_prescription(prescription_id, prescription_data):
            # Cập nhật số lượng trong Combobox
            available_quantity = medicine_quantity_dict[ten_thuoc] - int(quantity_entry.get())
            medicine_quantity_dict[ten_thuoc] = available_quantity
            new_display = [f"{name.split(' (')[0]} (Số lượng: {medicine_quantity_dict[name.split(' (')[0]]})" for name in medicine_display]
            medicine_entry.configure(values=new_display)
            load_prescriptions()
            clear_form()

    # Xử lý xóa đơn thuốc
    def delete_prescription_handler():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn đơn thuốc để xóa!")
            return
        prescription_id = tree.item(selected_item[0])["values"][0]
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa đơn thuốc này không?")
        if confirm:
            if prescription_controller_instance.delete_prescription(prescription_id):
                # Cập nhật số lượng trong Combobox
                selected_item = tree.item(tree.selection()[0])["values"]
                danh_sach_thuoc = selected_item[4]
                parts = danh_sach_thuoc.split(",")
                ten_thuoc = parts[0].strip()
                quantity_part = parts[1].strip() if len(parts) > 1 else "1"
                quantity = int(re.search(r'\d+', quantity_part).group())
                available_quantity = medicine_quantity_dict[ten_thuoc] + quantity
                medicine_quantity_dict[ten_thuoc] = available_quantity
                new_display = [f"{name.split(' (')[0]} (Số lượng: {medicine_quantity_dict[name.split(' (')[0]]})" for name in medicine_display]
                medicine_entry.configure(values=new_display)
                load_prescriptions()
                clear_form()

    # Xử lý tìm kiếm
    def search_prescription_handler():
        keyword = search_entry.get().strip()
        field = search_field.get()
        if not keyword or not field:
            load_prescriptions()
            return
        prescriptions = prescription_controller_instance.search_prescriptions(keyword, field)
        load_prescriptions(prescriptions)

    # Xử lý sự kiện khi người dùng chọn một dòng trong bảng
    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item[0])["values"]
            appointment_id = item[1]
            for display, appt_id in appointment_dict.items():
                if appt_id == appointment_id:
                    appointment_entry.set(display)
                    break
            danh_sach_thuoc = item[4]
            parts = danh_sach_thuoc.split(",")
            ten_thuoc = parts[0].strip()
            quantity_part = parts[1].strip() if len(parts) > 1 else "1"
            quantity = re.search(r'\d+', quantity_part).group()
            duration_part = parts[2].strip() if len(parts) > 2 else ""
            for display in medicine_display:
                if ten_thuoc in display:
                    medicine_entry.set(display)
                    break
            quantity_entry.delete(0, ctk.END)
            quantity_entry.insert(0, quantity)
            duration_entry.delete(0, ctk.END)
            duration_entry.insert(0, duration_part)
            instruction_entry.delete(0, ctk.END)
            instruction_entry.insert(0, item[5] if item[5] else "")

    # Tiêu đề
    title_label = ctk.CTkLabel(frame, text="Quản lý Kê Đơn", font=("Arial", 18, "bold"))
    title_label.pack(pady=10)

    # Form nhập thông tin kê đơn
    content_frame = ctk.CTkFrame(frame)
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    input_frame = ctk.CTkFrame(content_frame, width=300)
    input_frame.pack(side="left", padx=10, pady=5, fill="y")

    # Tạo các ô nhập liệu
    ctk.CTkLabel(input_frame, text="Lịch hẹn:", font=("Arial", 12)).pack(pady=5, anchor="w")
    appointment_entry = ctk.CTkComboBox(input_frame, values=appointment_display, width=250)
    appointment_entry.pack(pady=5)

    ctk.CTkLabel(input_frame, text="Thuốc:", font=("Arial", 12)).pack(pady=5, anchor="w")
    medicine_entry = ctk.CTkComboBox(input_frame, values=medicine_display, width=250)
    medicine_entry.pack(pady=5)

    ctk.CTkLabel(input_frame, text="Số lượng:", font=("Arial", 12)).pack(pady=5, anchor="w")
    quantity_entry = ctk.CTkEntry(input_frame, width=250, placeholder_text="Nhập số lượng (ví dụ: 5)")
    quantity_entry.pack(pady=5)
    quantity_entry.bind("<KeyRelease>", check_quantity)

    ctk.CTkLabel(input_frame, text="Thời gian sử dụng:", font=("Arial", 12)).pack(pady=5, anchor="w")
    duration_entry = ctk.CTkEntry(input_frame, width=250, placeholder_text="Thời gian sử dụng (ví dụ: 3 ngày)")
    duration_entry.pack(pady=5)

    ctk.CTkLabel(input_frame, text="Hướng dẫn:", font=("Arial", 12)).pack(pady=5, anchor="w")
    instruction_entry = ctk.CTkEntry(input_frame, width=250, placeholder_text="Hướng dẫn (ví dụ: Uống sau ăn)")
    instruction_entry.pack(pady=5)

    # Frame bên phải: Chứa bảng và nút chức năng
    right_frame = ctk.CTkFrame(content_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

    # Ô tìm kiếm
    search_frame = ctk.CTkFrame(right_frame)
    search_frame.pack(fill="x", pady=5, padx=10)

    ctk.CTkLabel(search_frame, text="Tìm kiếm:", font=("Arial", 12)).pack(side="left", padx=5)
    search_entry = ctk.CTkEntry(search_frame, width=200, placeholder_text="Nhập từ khóa tìm kiếm...")
    search_entry.pack(side="left", padx=5)

    search_field = ctk.CTkComboBox(search_frame, values=["ID Lịch hẹn", "Tên thú cưng", "Tên bác sĩ", "Ngày kê đơn"], width=150)
    search_field.pack(side="left", padx=5)

    # Hiển thị danh sách đơn thuốc trong bảng
    table_frame = ctk.CTkFrame(right_frame)
    table_frame.pack(fill="both", expand=True, pady=5)

    columns = ("id", "id_lich_hen", "ten_thu_cung", "ten_bac_si", "danh_sach_thuoc", "huong_dan", "ngay_ke_don")
    tree = Treeview(table_frame, columns=columns, show="headings", height=15)

    for col, text, width in [
        ("id", "ID", 30),
        ("id_lich_hen", "ID Lịch hẹn", 70),
        ("ten_thu_cung", "Tên thú cưng", 150),
        ("ten_bac_si", "Tên bác sĩ", 150),
        ("danh_sach_thuoc", "Danh sách thuốc", 200),
        ("huong_dan", "Hướng dẫn", 200),
        ("ngay_ke_don", "Ngày kê đơn", 150),
    ]:
        tree.heading(col, text=text)
        tree.column(col, width=width)

    tree.pack(fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # Frame cho các nút chức năng
    button_frame = ctk.CTkFrame(right_frame)
    button_frame.pack(fill="x", padx=10, pady=5)

    prescribe_button = ctk.CTkButton(button_frame, text="Thêm ", command=prescribe_handler, width=120)
    prescribe_button.pack(side="left", padx=5)

    edit_button = ctk.CTkButton(button_frame, text="Sửa", command=edit_prescription_handler, width=120)
    edit_button.pack(side="left", padx=5)

    delete_button = ctk.CTkButton(button_frame, text="Xóa", command=delete_prescription_handler, width=120)
    delete_button.pack(side="left", padx=5)

    search_button = ctk.CTkButton(button_frame, text="Tìm kiếm", command=search_prescription_handler, width=120)
    search_button.pack(side="left", padx=5)

    # Tải dữ liệu ban đầu
    load_prescriptions()