import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview, Style
from tkcalendar import DateEntry
import controllers.appointment_controller as appointment_controller

def open_appointment_content(frame):
    controller = appointment_controller.ManageAppointmentController()

    # Lấy danh sách bác sĩ để hiển thị trong combobox
    doctors = controller.get_doctors()
    doctor_names = [doctor[1] for doctor in doctors]  # Lấy danh sách tên bác sĩ

    title_label = ctk.CTkLabel(frame, text="Quản lý Lịch hẹn", font=("Arial", 18, "bold"), text_color="black")
    title_label.pack(pady=10)

    content_frame = ctk.CTkFrame(frame)
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    input_frame = ctk.CTkFrame(content_frame, width=300)
    input_frame.pack(side="left", padx=10, pady=5, fill="y")

    entries = {}
    fields = ["Thú cưng hẹn", "Tên thú cưng", "Tên chủ sở hữu", "Ngày hẹn", "Giờ hẹn", "Trạng thái", "Bác sĩ khám"]

    for field in fields:
        ctk.CTkLabel(input_frame, text=f"{field}:", font=("Arial", 12)).pack(pady=5, anchor="w")

        if field == "Ngày hẹn":
            date_entry = DateEntry(input_frame, width=25, date_pattern='yyyy-MM-dd')
            date_entry.pack(pady=5, ipady=8, fill="x", padx=5)
            entries[field] = date_entry

        elif field == "Giờ hẹn":
            time_frame = ctk.CTkFrame(input_frame)
            time_frame.pack(pady=5, fill="x", padx=5)

            hour_combobox = ctk.CTkComboBox(time_frame, values=[f"{i:02d}" for i in range(24)], width=80)
            hour_combobox.set("00")
            hour_combobox.pack(side="left", padx=5)

            minute_combobox = ctk.CTkComboBox(time_frame, values=[f"{i:02d}" for i in range(60)], width=80)
            minute_combobox.set("00")
            minute_combobox.pack(side="left", padx=5)

            entries[field] = (hour_combobox, minute_combobox)

        elif field == "Trạng thái":
            status_combobox = ctk.CTkComboBox(input_frame, values=["Chờ xác nhận", "Đã xác nhận", "Đã hoàn thành", "Đã hủy"], width=250)
            status_combobox.pack(pady=5, fill="x", padx=5)
            entries[field] = status_combobox

        elif field == "Bác sĩ khám":
            doctor_combobox = ctk.CTkComboBox(input_frame, values=doctor_names, width=250)
            doctor_combobox.pack(pady=5, fill="x", padx=5)
            entries[field] = doctor_combobox

        else:
            entry = ctk.CTkEntry(input_frame, width=250)
            entry.pack(pady=5, fill="x", padx=5)
            entries[field] = entry

    right_frame = ctk.CTkFrame(content_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

    search_frame = ctk.CTkFrame(right_frame)
    search_frame.pack(fill="x", pady=(0, 5))

    ctk.CTkLabel(search_frame, text="Tìm kiếm:", font=("Arial", 12)).pack(side="left", padx=(0, 5))

    search_entry = ctk.CTkEntry(search_frame, width=150, placeholder_text="Tên thú cưng, chủ sở hữu, hoặc bác sĩ...")
    search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

    ctk.CTkLabel(search_frame, text="Từ ngày:", font=("Arial", 12)).pack(side="left", padx=(5, 0))
    start_date_entry = DateEntry(search_frame, width=12, date_pattern='yyyy-MM-dd')
    start_date_entry.pack(side="left", padx=(0, 5))

    ctk.CTkLabel(search_frame, text="Đến ngày:", font=("Arial", 12)).pack(side="left", padx=(5, 0))
    end_date_entry = DateEntry(search_frame, width=12, date_pattern='yyyy-MM-dd')
    end_date_entry.pack(side="left", padx=(0, 5))

    def perform_search():
        keyword = search_entry.get().strip()
        start_date = start_date_entry.get_date()
        end_date = end_date_entry.get_date()

        conditions = {}

        if start_date:
            conditions["ngay_hen >="] = start_date.strftime('%Y-%m-%d')
        if end_date:
            conditions["ngay_hen <="] = end_date.strftime('%Y-%m-%d')
        if keyword:
            conditions["keyword"] = keyword

        try:
            appointments = controller.search_appointments(conditions)
            tree.delete(*tree.get_children())
            for appt in appointments:
                tree.insert("", "end", values=(
                    appt["id"],
                    appt["ten_thu_cung"],
                    appt["id_thu_cung"],
                    appt["ten_chu_so_huu"],
                    appt["ngay_hen"],
                    appt["gio_hen"],
                    appt["trang_thai"],
                    appt["ten_bac_si"]
                ))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {str(e)}")

    table_frame = ctk.CTkFrame(right_frame)
    table_frame.pack(fill="both", expand=True, pady=5)

    style = Style()
    style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
    style.configure("Treeview", font=("Arial", 12))

    columns = ("appointment_id", "ten_thu_cung", "id_thu_cung", "ten_chu_so_huu", "date", "time", "status", "ten_bac_si")
    tree = Treeview(table_frame, columns=columns, show="headings", height=15)

    for col, text in zip(columns, ["ID Lịch hẹn", "Tên thú cưng", "ID Thú cưng", "Tên chủ sở hữu", "Ngày hẹn", "Giờ hẹn", "Trạng thái", "Bác sĩ khám"]):
        tree.heading(col, text=text)
        tree.column(col, width=120)

    tree.pack(fill="both", expand=True)

    # Hàm xử lý khi chọn dòng trong bảng
    def on_tree_select(event):
        selected_item = tree.selection()
        if not selected_item:
            return

        # Lấy dữ liệu từ dòng được chọn
        item = tree.item(selected_item)
        values = item["values"]

        # Điền dữ liệu vào các ô nhập liệu
        entries["Thú cưng hẹn"].delete(0, "end")
        entries["Thú cưng hẹn"].insert(0, values[2])  # id_thu_cung
        entries["Tên thú cưng"].delete(0, "end")
        entries["Tên thú cưng"].insert(0, values[1])
        entries["Tên chủ sở hữu"].delete(0, "end")
        entries["Tên chủ sở hữu"].insert(0, values[3])
        entries["Ngày hẹn"].set_date(values[4])
        hour, minute = values[5].split(":")[:2]
        entries["Giờ hẹn"][0].set(hour)
        entries["Giờ hẹn"][1].set(minute)
        entries["Trạng thái"].set(values[6])
        entries["Bác sĩ khám"].set(values[7])

    # Gắn sự kiện vào bảng
    tree.bind("<<TreeviewSelect>>", on_tree_select)

    def handle_action(action):
        try:
            ngay_hen = entries["Ngày hẹn"].get_date()
            gio_hen_hour = entries["Giờ hẹn"][0].get()
            gio_hen_minute = entries["Giờ hẹn"][1].get()

            if not ngay_hen:
                messagebox.showwarning("Cảnh báo", "Ngày hẹn không được để trống!")
                return
            if not gio_hen_hour or not gio_hen_minute:
                messagebox.showwarning("Cảnh báo", "Giờ hẹn không được để trống!")
                return

            gio_hen = f"{gio_hen_hour}:{gio_hen_minute}:00"

            # Lấy ID bác sĩ từ tên bác sĩ
            doctor_name = entries["Bác sĩ khám"].get()
            doctor_id = controller.get_doctor_id_by_name(doctor_name)
            if not doctor_id:
                messagebox.showwarning("Cảnh báo", f"Bác sĩ {doctor_name} không tồn tại!")
                return

            appointment_data = {
                "id_thu_cung": entries["Thú cưng hẹn"].get(),
                "ngay_hen": ngay_hen.strftime('%Y-%m-%d'),
                "gio_hen": gio_hen,
                "trang_thai": entries["Trạng thái"].get(),
                "id_bac_si": doctor_id
            }

            if action == "add":
                controller.add_appointment(appointment_data)
            elif action == "update":
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn lịch hẹn để cập nhật!")
                    return
                appointment_data["id"] = tree.item(selected_item)['values'][0]
                controller.update_appointment(appointment_data)
            elif action == "delete":
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn lịch hẹn để xóa!")
                    return
                controller.delete_appointment(tree.item(selected_item)['values'][0])

            display_appointments()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    def display_appointments():
        tree.delete(*tree.get_children())
        appointments = controller.get_all_appointments()
        for appointment in appointments:
            tree.insert("", "end", values=(
                appointment[0],  # id
                appointment[2],  # ten_thu_cung
                appointment[1],  # id_thu_cung
                appointment[3],  # ten_chu_so_huu
                appointment[4],  # ngay_hen
                appointment[5],  # gio_hen
                appointment[6],  # trang_thai
                appointment[7]   # ten_bac_si
            ))

    button_frame = ctk.CTkFrame(right_frame)
    button_frame.pack(fill="x", padx=10, pady=5)

    add_button = ctk.CTkButton(button_frame, text="Add", command=lambda: handle_action("add"), width=120)
    add_button.pack(side="left", padx=5)

    update_button = ctk.CTkButton(button_frame, text="Update", command=lambda: handle_action("update"), width=120)
    update_button.pack(side="left", padx=5)

    delete_button = ctk.CTkButton(button_frame, text="Delete", command=lambda: handle_action("delete"), width=120)
    delete_button.pack(side="left", padx=5)

    search_button = ctk.CTkButton(button_frame, text="Search", command=lambda: perform_search(), width=120)
    search_button.pack(side="left", padx=5)

    display_appointments()