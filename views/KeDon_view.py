import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview
import controllers.KeDon_controller as prescription_controller
import re
import threading

def open_manage_prescription_content(frame):
    controller = prescription_controller.PrescriptionController()

    # Lấy dữ liệu ban đầu
    appointments = controller.get_appointments()
    appointment_display = [f"ID: {appt[0]} - {appt[1]} (BS: {appt[2]}) - {appt[3]} {appt[4]}" for appt in appointments]
    appointment_dict = {display: appt[0] for display, appt in zip(appointment_display, appointments)}

    medicines = controller.get_medicines()
    medicine_display = [f"{medicine[1]} (Số lượng: {medicine[2] if medicine[2] is not None else 0})" for medicine in medicines]
    medicine_dict = {display: medicine[1] for display, medicine in zip(medicine_display, medicines)}
    medicine_quantity_dict = {medicine[1]: medicine[2] if medicine[2] is not None else 0 for medicine in medicines}

    # Hàm tiện ích
    def clear_form():
        appointment_entry.set("")
        medicine_entry.set("")
        quantity_entry.delete(0, ctk.END)
        duration_entry.delete(0, ctk.END)
        instruction_entry.delete(0, ctk.END)

    def load_prescriptions(prescriptions=None):
        for item in tree.get_children():
            tree.delete(item)
        if prescriptions is None:
            prescriptions = controller.get_all_prescriptions()
        for prescription in prescriptions:
            tree.insert("", "end", values=prescription)

    def check_quantity(*args):
        selected_medicine = medicine_dict.get(medicine_entry.get())
        if not selected_medicine:
            return
        try:
            quantity = int(quantity_entry.get())
            available = medicine_quantity_dict.get(selected_medicine, 0)
            if quantity > available:
                messagebox.showwarning("Cảnh báo", f"Số lượng trong kho không đủ! Hiện có: {available}")
                quantity_entry.delete(0, ctk.END)
                quantity_entry.insert(0, str(available))
        except ValueError:
            pass

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

        def prescribe_async():
            try:
                if controller.prescribe_medicine(prescription_data):
                    available = medicine_quantity_dict[ten_thuoc] - int(quantity_entry.get())
                    medicine_quantity_dict[ten_thuoc] = available
                    new_display = [f"{name.split(' (')[0]} (Số lượng: {medicine_quantity_dict[name.split(' (')[0]]})" for name in medicine_display]
                    frame.after(0, lambda: medicine_entry.configure(values=new_display))
                    frame.after(0, load_prescriptions)
                    frame.after(0, clear_form)
            except Exception as e:
                frame.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi khi kê đơn: {e}"))

        threading.Thread(target=prescribe_async, daemon=True).start()

    # Xử lý sửa đơn thuốc
    def edit_prescription_handler():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn đơn thuốc để sửa!")
            return
        prescription_id = tree.item(selected[0])["values"][0]
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

        def edit_async():
            try:
                if controller.update_prescription(prescription_id, prescription_data):
                    available = medicine_quantity_dict[ten_thuoc] - int(quantity_entry.get())
                    medicine_quantity_dict[ten_thuoc] = available
                    new_display = [f"{name.split(' (')[0]} (Số lượng: {medicine_quantity_dict[name.split(' (')[0]]})" for name in medicine_display]
                    frame.after(0, lambda: medicine_entry.configure(values=new_display))
                    frame.after(0, load_prescriptions)
                    frame.after(0, clear_form)
            except Exception as e:
                frame.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi khi cập nhật: {e}"))

        threading.Thread(target=edit_async, daemon=True).start()

    # Xử lý xóa đơn thuốc
    def delete_prescription_handler():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn đơn thuốc để xóa!")
            return
        prescription_id = tree.item(selected[0])["values"][0]
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa đơn thuốc này không?"):
            return

        def delete_async():
            try:
                if controller.delete_prescription(prescription_id):
                    selected_item = tree.item(tree.selection()[0])["values"]
                    parts = selected_item[4].split(",")
                    ten_thuoc = parts[0].strip() if parts else ""
                    quantity_part = parts[1].strip() if len(parts) > 1 else "1"
                    match = re.search(r'\d+', quantity_part)
                    quantity = int(match.group()) if match else 1
                    if ten_thuoc in medicine_quantity_dict:
                        available = medicine_quantity_dict[ten_thuoc] + quantity
                        medicine_quantity_dict[ten_thuoc] = available
                        new_display = [f"{name.split(' (')[0]} (Số lượng: {medicine_quantity_dict[name.split(' (')[0]]})" for name in medicine_display]
                        frame.after(0, lambda: medicine_entry.configure(values=new_display))
                        frame.after(0, load_prescriptions)
                        frame.after(0, clear_form)
            except Exception as e:
                frame.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi khi xóa: {e}"))

        threading.Thread(target=delete_async, daemon=True).start()

    # Xử lý tìm kiếm
    def search_prescription_handler():
        keyword = search_entry.get().strip()
        field = search_field.get()
        if not keyword or not field:
            load_prescriptions()
            return

        def search_async():
            try:
                prescriptions = controller.search_prescriptions(keyword, field)
                frame.after(0, lambda: load_prescriptions(prescriptions))
            except Exception as e:
                frame.after(0, lambda: messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {e}"))

        threading.Thread(target=search_async, daemon=True).start()

    # Xử lý sự kiện chọn dòng trong bảng
    def on_tree_select(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])["values"]
            for display, appt_id in appointment_dict.items():
                if appt_id == item[1]:
                    appointment_entry.set(display)
                    break
            parts = item[4].split(",")
            ten_thuoc = parts[0].strip() if parts else ""
            quantity_part = parts[1].strip() if len(parts) > 1 else "1"
            match = re.search(r'\d+', quantity_part)
            quantity = match.group() if match else "1"
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

    # Giao diện
    ctk.CTkLabel(frame, text="Quản lý Kê Đơn", font=("Arial", 18, "bold")).pack(pady=10)

    content_frame = ctk.CTkFrame(frame)
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    input_frame = ctk.CTkFrame(content_frame, width=300)
    input_frame.pack(side="left", padx=10, pady=5, fill="y")

    # Ô nhập liệu
    labels = ["Lịch hẹn:", "Thuốc:", "Số lượng:", "Thời gian sử dụng:", "Hướng dẫn:"]
    entries = []
    for label in labels:
        ctk.CTkLabel(input_frame, text=label, font=("Arial", 12)).pack(pady=5, anchor="w")
        if label == "Lịch hẹn:":
            entry = ctk.CTkComboBox(input_frame, values=appointment_display, width=250)
        elif label == "Thuốc:":
            entry = ctk.CTkComboBox(input_frame, values=medicine_display, width=250)
        else:
            placeholder = "Nhập số lượng (ví dụ: 5)" if label == "Số lượng:" else "Thời gian sử dụng (ví dụ: 3 ngày)" if label == "Thời gian sử dụng:" else "Hướng dẫn (ví dụ: Uống sau ăn)"
            entry = ctk.CTkEntry(input_frame, width=250, placeholder_text=placeholder)
        entry.pack(pady=5)
        entries.append(entry)

    appointment_entry, medicine_entry, quantity_entry, duration_entry, instruction_entry = entries
    quantity_entry.bind("<KeyRelease>", check_quantity)

    # Frame bên phải
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

    # Bảng hiển thị
    table_frame = ctk.CTkFrame(right_frame)
    table_frame.pack(fill="both", expand=True, pady=5)

    columns = ("id", "id_lich_hen", "ten_thu_cung", "ten_bac_si", "danh_sach_thuoc", "huong_dan", "ngay_ke_don")
    tree = Treeview(table_frame, columns=columns, show="headings", height=15)
    column_configs = [
        ("id", "ID", 30),
        ("id_lich_hen", "ID Lịch hẹn", 70),
        ("ten_thu_cung", "Tên thú cưng", 150),
        ("ten_bac_si", "Tên bác sĩ", 150),
        ("danh_sach_thuoc", "Danh sách thuốc", 200),
        ("huong_dan", "Hướng dẫn", 200),
        ("ngay_ke_don", "Ngày kê đơn", 150),
    ]
    for col, text, width in column_configs:
        tree.heading(col, text=text)
        tree.column(col, width=width)
    tree.pack(fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # Nút chức năng
    button_frame = ctk.CTkFrame(right_frame)
    button_frame.pack(fill="x", padx=10, pady=5)

    buttons = [
        ("Thêm", prescribe_handler),
        ("Sửa", edit_prescription_handler),
        ("Xóa", delete_prescription_handler),
        ("Tìm kiếm", search_prescription_handler)
    ]
    for text, command in buttons:
        ctk.CTkButton(button_frame, text=text, command=command, width=120).pack(side="left", padx=5)

    load_prescriptions()