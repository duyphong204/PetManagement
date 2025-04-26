import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview, Style
from tkcalendar import DateEntry
import controllers.disease_treatment_controller as treatment_controller

def open_treatment_content(frame):
    controller = treatment_controller.ManageTreatmentController()

    # Tiêu đề
    title_label = ctk.CTkLabel(frame, text="Quản lý Điều trị", font=("Arial", 18, "bold"), text_color="black")
    title_label.pack(pady=10)

    # Frame chính
    content_frame = ctk.CTkFrame(frame)
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # === INPUT FORM ===
    input_frame = ctk.CTkFrame(content_frame, width=300)
    input_frame.pack(side="left", padx=10, pady=5, fill="y")

    entries = {}
    fields = ["ID Lịch hẹn", "Thú cưng điều trị", "Bác sĩ điều trị", "Ngày điều trị", "Chẩn đoán", "Đơn thuốc", "Chi phí"]

    for field in fields:
        ctk.CTkLabel(input_frame, text=f"{field}:", font=("Arial", 12)).pack(pady=5, anchor="w")
        if field == "Ngày điều trị":
            date_entry = DateEntry(input_frame, width=25, date_pattern='yyyy-MM-dd')
            date_entry.pack(pady=5, ipady=8, fill="x", padx=5)
            entries[field] = date_entry
        else:
            entry = ctk.CTkEntry(input_frame, width=250)
            entry.pack(pady=5, fill="x", padx=5)
            entries[field] = entry

    # === RIGHT SIDE ===
    right_frame = ctk.CTkFrame(content_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

    # === SEARCH BAR ===
    search_frame = ctk.CTkFrame(right_frame)
    search_frame.pack(fill="x", pady=(0, 5))

    ctk.CTkLabel(search_frame, text="Tìm kiếm:", font=("Arial", 12)).pack(side="left", padx=(0, 5))
    search_entry = ctk.CTkEntry(search_frame, width=150, placeholder_text="Nhập từ khóa tìm kiếm...")
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
            conditions["ngay_dieu_tri >="] = start_date.strftime('%Y-%m-%d')
        if end_date:
            conditions["ngay_dieu_tri <="] = end_date.strftime('%Y-%m-%d')
        if keyword:
            conditions["keyword"] = keyword

        try:
            treatments = controller.search_treatments(conditions)
            tree.delete(*tree.get_children())
            for treatment in treatments:
                tree.insert("", "end", values=(
                    treatment["id"],
                    treatment["id_lich_hen"],
                    treatment["id_thu_cung"],
                    treatment["id_bac_si"],
                    treatment["ngay_dieu_tri"],
                    treatment["chan_doan"],
                    treatment["don_thuoc"],
                    treatment["chi_phi"]
                ))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {str(e)}")

    # === TABLE ===
    table_frame = ctk.CTkFrame(right_frame)
    table_frame.pack(fill="both", expand=True, pady=5)

    style = Style()
    style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
    style.configure("Treeview", font=("Arial", 12))

    columns = ("treatment_id", "appointment_id", "pet_id", "doctor_id", "treatment_date", "diagnosis", "prescription", "cost")
    tree = Treeview(table_frame, columns=columns, show="headings", height=15)

    tree_headers = ["ID Điều trị", "ID Lịch hẹn", "Thú cưng điều trị", "Bác sĩ điều trị", "Ngày điều trị", "Chẩn đoán", "Đơn thuốc", "Chi phí"]
    for col, text in zip(columns, tree_headers):
        tree.heading(col, text=text)
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True)

    # Hàm xử lý khi chọn dòng trong bảng
    def on_tree_select(event):
        selected_item = tree.selection()
        if not selected_item:
            return

        item = tree.item(selected_item)
        values = item["values"]

        entries["ID Lịch hẹn"].delete(0, ctk.END)
        entries["ID Lịch hẹn"].insert(0, values[1] or "")

        entries["Thú cưng điều trị"].delete(0, ctk.END)
        entries["Thú cưng điều trị"].insert(0, values[2])

        entries["Bác sĩ điều trị"].delete(0, ctk.END)
        entries["Bác sĩ điều trị"].insert(0, values[3])

        entries["Ngày điều trị"].set_date(values[4])

        entries["Chẩn đoán"].delete(0, ctk.END)
        entries["Chẩn đoán"].insert(0, values[5])

        entries["Đơn thuốc"].delete(0, ctk.END)
        entries["Đơn thuốc"].insert(0, values[6])

        entries["Chi phí"].delete(0, ctk.END)
        entries["Chi phí"].insert(0, values[7])

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    def handle_action(action):
        try:
            treatment_data = {
                "id_lich_hen": entries["ID Lịch hẹn"].get().strip() or None,
                "id_thu_cung": entries["Thú cưng điều trị"].get(),
                "id_bac_si": entries["Bác sĩ điều trị"].get(),
                "ngay_dieu_tri": entries["Ngày điều trị"].get_date().strftime("%Y-%m-%d"),
                "chan_doan": entries["Chẩn đoán"].get(),
                "don_thuoc": entries["Đơn thuốc"].get(),
                "chi_phi": entries["Chi phí"].get()
            }

            if not treatment_data["id_thu_cung"]:
                messagebox.showwarning("Cảnh báo", "Thú cưng điều trị không được để trống!")
                return
            if not treatment_data["id_bac_si"]:
                messagebox.showwarning("Cảnh báo", "Bác sĩ điều trị không được để trống!")
                return
            if not treatment_data["ngay_dieu_tri"]:
                messagebox.showwarning("Cảnh báo", "Ngày điều trị không được để trống!")
                return
            if not treatment_data["chan_doan"]:
                messagebox.showwarning("Cảnh báo", "Chẩn đoán không được để trống!")
                return
            if not treatment_data["don_thuoc"]:
                messagebox.showwarning("Cảnh báo", "Đơn thuốc không được để trống!")
                return
            if not treatment_data["chi_phi"]:
                messagebox.showwarning("Cảnh báo", "Chi phí không được để trống!")
                return

            if action == "add":
                controller.add_treatment(treatment_data)
            elif action == "update":
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn điều trị để cập nhật!")
                    return
                treatment_data["id"] = tree.item(selected_item)['values'][0]
                controller.update_treatment(treatment_data)
            elif action == "delete":
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn điều trị để xóa!")
                    return
                controller.delete_treatment(tree.item(selected_item)['values'][0])

            display_treatments()
            clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")

    def display_treatments():
        tree.delete(*tree.get_children())
        treatments = controller.get_all_treatments()
        for treatment in treatments:
            tree.insert("", "end", values=(
                treatment["id"],
                treatment["id_lich_hen"],
                treatment["id_thu_cung"],
                treatment["id_bac_si"],
                treatment["ngay_dieu_tri"],
                treatment["chan_doan"],
                treatment["don_thuoc"],
                treatment["chi_phi"]
            ))

    # === BUTTONS ===
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

    def clear_form():
        for field, entry in entries.items():
            if field == "Ngày điều trị":
                entry.set_date("2024-01-01")
            else:
                entry.delete(0, ctk.END)

    # Hiển thị dữ liệu ban đầu
    display_treatments()