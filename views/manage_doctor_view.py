import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview, Style
import controllers.quanlybacsi_controller as doctor_controller
import controllers.quanlybacsi_dieutri_controller as treatment_controller 

def open_manage_doctor_content(frame):
    doctor_controller_instance = doctor_controller.DoctorController()
    treatment_controller_instance = treatment_controller.TreatmentController() 

    title_label = ctk.CTkLabel(frame, text="Quản lý Bác sĩ", font=("Arial", 18, "bold"), text_color="black")
    title_label.pack(pady=10)

    # Frame chính chứa nội dung
    content_frame = ctk.CTkFrame(frame)
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Frame chứa nút điều hướng (Thông tin bác sĩ & Điều trị)
    nav_frame = ctk.CTkFrame(content_frame, width=150)
    nav_frame.pack(side="left", padx=10, pady=5, fill="y")

    # Nút "Thông tin bác sĩ"
    btn_doctor_info = ctk.CTkButton(nav_frame, text="Thông tin bác sĩ", font=("Arial", 14), hover_color="#2C3E50", width=140, command=lambda: show_section('doctor_info'))
    btn_doctor_info.pack(pady=5)

    # Nút "Điều trị"
    btn_treatment = ctk.CTkButton(nav_frame, text="Điều trị", font=("Arial", 14), hover_color="#2C3E50", width=140, command=lambda: show_section('treatment'))
    btn_treatment.pack(pady=5)

    # Frame bên trái: Chứa ô nhập liệu cho Thông tin bác sĩ
    input_frame = ctk.CTkFrame(content_frame, width=200)
    input_frame.pack(side="left", padx=10, pady=5, fill="y")


    doctor_entries = {}
    doctor_fields = ["Họ tên", "Chuyên môn", "Số điện thoại", "Email", "ID Người Dùng"]
    
    for field in doctor_fields:
        ctk.CTkLabel(input_frame, text=f"{field}:", font=("Arial", 12)).pack(pady=5, anchor="w")
        
        if field == "ID Người Dùng":
            entry = ctk.CTkEntry(input_frame, width=250, validate="key", validatecommand=(frame.register(validate_id), "%P"))
        else:
            entry = ctk.CTkEntry(input_frame, width=250)
        
        entry.pack(pady=5)
        doctor_entries[field] = entry

    # Frame bên phải: Chứa bảng và nút chức năng (bác sĩ và điều trị)
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

    # Tạo bảng Treeview cho bác sĩ
    doctor_columns = ("id", "ho_ten", "chuyen_mon", "so_dien_thoai", "email", "id_nguoi_dung")
    doctor_tree = Treeview(table_frame, columns=doctor_columns, show="headings", height=15, style="Treeview")
    
    for col, text in zip(doctor_columns, ["ID", "Họ tên", "Chuyên môn", "Số điện thoại", "Email", "ID Người dùng"]):
        doctor_tree.heading(col, text=text)

    doctor_tree.column("id", width=50)
    doctor_tree.column("ho_ten", width=150)
    doctor_tree.column("chuyen_mon", width=200)
    doctor_tree.column("so_dien_thoai", width=150)
    doctor_tree.column("email", width=200)
    doctor_tree.column("id_nguoi_dung", width=120)

    doctor_tree.pack(fill="both", expand=True)

    # Frame nút chức năng
    button_frame = ctk.CTkFrame(right_frame)
    button_frame.pack(fill="x", padx=10, pady=5)

    # Hiển thị dữ liệu lên bảng
    def display_doctors(doctors):
        for item in doctor_tree.get_children():
            doctor_tree.delete(item)
        if doctors:
            for doctor in doctors:
                if len(doctor) == 6:
                    doctor_tree.insert("", "end", values=doctor)
        else:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị.")

    # Chọn một dòng trong bảng
    def on_tree_select(event):
        selected_item = doctor_tree.selection()
        if selected_item:
            item = doctor_tree.item(selected_item[0])["values"]
            for i, (field, entry) in enumerate(doctor_entries.items(), start=1):
                entry.delete(0, ctk.END)
                entry.insert(0, item[i] if item[i] else "")

    doctor_tree.bind("<<TreeviewSelect>>", on_tree_select)

    def search_doctor():
        keyword = search_entry.get().strip()
        doctors = doctor_controller_instance.search_doctors(keyword)
        display_doctors(doctors)
        if not doctors and keyword:
            messagebox.showinfo("Thông báo", "Không tìm thấy bác sĩ.")

    # Xử lý các thao tác (Add, Update, Delete) cho bác sĩ
    def handle_doctor_action(action, success_message):
        try:
            doctor_data = {field: entry.get() for field, entry in doctor_entries.items()}
            if action in ["add", "update"]:
                for field, value in doctor_data.items():
                    if not value and field != "ID Người Dùng":
                        messagebox.showwarning("Cảnh báo", f"Vui lòng nhập {field}.")
                        return
                phone_number = doctor_data.get("Số điện thoại", "")
                if phone_number and not phone_number.startswith("0"):
                    doctor_data["Số điện thoại"] = "0" + phone_number
            if action == "add":
                if doctor_controller_instance.add_doctor(doctor_data):
                    messagebox.showinfo("Thành công", success_message)
            elif action == "update":
                selected_item = doctor_tree.selection()
                if not selected_item:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn bác sĩ để cập nhật!")
                    return
                doctor_id = doctor_tree.item(selected_item[0])["values"][0]
                if doctor_controller_instance.update_doctor(doctor_id, doctor_data):
                    messagebox.showinfo("Thành công", success_message)
            elif action == "delete":
                selected_item = doctor_tree.selection()
                if not selected_item:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn bác sĩ để xóa!")
                    return
                doctor_id = doctor_tree.item(selected_item[0])["values"][0]
                confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa bác sĩ này không?")
                if confirm and doctor_controller_instance.delete_doctor(doctor_id):
                    messagebox.showinfo("Thành công", success_message)

            # Cập nhật lại bảng sau khi thực hiện hành động
            doctors = doctor_controller_instance.get_all_doctors()
            display_doctors(doctors)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi {action}: {e}")

    # Nút chức năng của bác sĩ
    ctk.CTkButton(search_frame, text="Tìm", command=search_doctor, width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Thêm bác sĩ", command=lambda: handle_doctor_action("add", "Thêm bác sĩ thành công!"), width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Cập nhật bác sĩ", command=lambda: handle_doctor_action("update", "Cập nhật bác sĩ thành công!"), width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Xóa bác sĩ", command=lambda: handle_doctor_action("delete", "Xóa bác sĩ thành công!"), width=120).pack(side="left", padx=5)


### Điều trị: Tạo thêm phần cho Điều trị ###
    treatment_input_frame = ctk.CTkFrame(content_frame, width=200)
    treatment_input_frame.pack(side="left", padx=10, pady=5, fill="y")
    #nút chức năng
    treatment_button_frame = ctk.CTkFrame(right_frame)
    treatment_button_frame.pack(fill="x", padx=10, pady=5)
    
    treatment_search_frame = ctk.CTkFrame(right_frame)
    treatment_search_frame.pack(fill="x", pady=5)
    ctk.CTkLabel(treatment_search_frame, text="Tìm kiếm:", font=("Arial", 12)).pack(side="left", padx=5)
    treatment_search_entry = ctk.CTkEntry(treatment_search_frame, width=200)
    treatment_search_entry.pack(side="left", padx=5)

    # Các ô nhập liệu cho Điều trị
    treatment_entries = {}
    treatment_fields = ["ID Thú cưng", "ID Bác sĩ", "Ngày điều trị", "Chẩn đoán", "Kê đơn thuốc", "Liều lượng", "Ghi chú", "Chi phí"]

    for field in treatment_fields:
        ctk.CTkLabel(treatment_input_frame, text=f"{field}:", font=("Arial", 12)).pack(pady=5, anchor="w")
        entry = ctk.CTkEntry(treatment_input_frame, width=180)
        entry.pack(pady=5)
        treatment_entries[field] = entry

    # Bảng điều trị
    treatment_table_frame = ctk.CTkFrame(right_frame)
    treatment_table_frame.pack(fill="both", expand=True, pady=5)

    treatment_columns = ("id", "id_thu_cung", "id_bac_si", "ngay_dieu_tri", "chan_doan", "ke_don_thuoc", "lieu_luong", "ghi_chu", "chi_phi")
    treatment_tree = Treeview(treatment_table_frame, columns=treatment_columns, show="headings", height=15, style="Treeview")
    
    for col, text in zip(treatment_columns, ["ID", "ID Thú cưng", "ID Bác sĩ", "Ngày điều trị", "Chẩn đoán", "Kê đơn thuốc", "Liều lượng", "Ghi chú", "Chi phí"]):
        treatment_tree.heading(col, text=text)

    treatment_tree.column("id", width=50)
    treatment_tree.column("id_thu_cung", width=100)
    treatment_tree.column("id_bac_si", width=100)
    treatment_tree.column("ngay_dieu_tri", width=150)
    treatment_tree.column("chan_doan", width=150)
    treatment_tree.column("ke_don_thuoc", width=150)
    treatment_tree.column("lieu_luong", width=120)
    treatment_tree.column("ghi_chu", width=150)
    treatment_tree.column("chi_phi", width=100)

    treatment_tree.pack(fill="both", expand=True)

   
    def search_treatment():
        keyword = treatment_search_entry.get().strip()
        treatments = treatment_controller_instance.search_treatments(keyword)
        display_treatments(treatments)

    # Hiển thị dữ liệu lên bảng điều trị
    def display_treatments(treatments):
        for item in treatment_tree.get_children():
            treatment_tree.delete(item)
        if treatments:
            for treatment in treatments:
                treatment_tree.insert("", "end", values=treatment)
        else:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị.")

    # Chọn một dòng trong bảng điều trị
    def on_treatment_tree_select(event):
        selected_item = treatment_tree.selection()
        if selected_item:
            item = treatment_tree.item(selected_item[0])["values"]
            for i, (field, entry) in enumerate(treatment_entries.items(), start=1):
                entry.delete(0, ctk.END)
                entry.insert(0, item[i] if item[i] else "")

    treatment_tree.bind("<<TreeviewSelect>>", on_treatment_tree_select)

    def handle_treatment_action(action, success_message):
        try:
            treatment_data = {field: entry.get() for field, entry in treatment_entries.items()}
            if action == "add":
                if treatment_controller_instance.add_treatment(treatment_data):
                    messagebox.showinfo("Thành công", success_message)
            elif action == "update":
                selected_item = treatment_tree.selection()
                if not selected_item:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn điều trị để cập nhật!")
                    return
                treatment_id = treatment_tree.item(selected_item[0])["values"][0]
                if treatment_controller_instance.update_treatment(treatment_id, treatment_data):
                    messagebox.showinfo("Thành công", success_message)
            elif action == "delete":
                selected_item = treatment_tree.selection()
                if not selected_item:
                    messagebox.showwarning("Cảnh báo", "Vui lòng chọn điều trị để xóa!")
                    return
                treatment_id = treatment_tree.item(selected_item[0])["values"][0]
                confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa điều trị này không?")
                if confirm and treatment_controller_instance.delete_treatment(treatment_id):
                    messagebox.showinfo("Thành công", success_message)

            treatments = treatment_controller_instance.get_all_treatments()
            display_treatments(treatments)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi {action}: {e}")

    # Nút chức năng cho điều trị
    ctk.CTkButton(treatment_search_frame, text="Tìm", command=search_treatment, width=120).pack(side="left", padx=5)
    ctk.CTkButton(treatment_button_frame, text="Thêm điều trị", command=lambda: handle_treatment_action("add", "Thêm điều trị thành công!"), width=120).pack(side="left", padx=5)
    ctk.CTkButton(treatment_button_frame, text="Cập nhật điều trị", command=lambda: handle_treatment_action("update", "Cập nhật điều trị thành công!"), width=120).pack(side="left", padx=5)
    ctk.CTkButton(treatment_button_frame, text="Xóa điều trị", command=lambda: handle_treatment_action("delete", "Xóa điều trị thành công!"), width=120).pack(side="left", padx=5)

   
    def show_section(section):
    # Ẩn tất cả các phần trước khi hiển thị phần mới
        input_frame.pack_forget()
        search_frame.pack_forget()
        table_frame.pack_forget()
        button_frame.pack_forget()
        treatment_input_frame.pack_forget()
        treatment_table_frame.pack_forget()
        treatment_search_frame.pack_forget()
        treatment_button_frame.pack_forget()

        if section == 'doctor_info':
        # Hiển thị phần thông tin bác sĩ
            input_frame.pack(side="left", padx=10, pady=5, fill="y")
            search_frame.pack(fill="x", pady=5)
            table_frame.pack(fill="both", expand=True, pady=5)
            button_frame.pack(fill="x", padx=10, pady=5)  # Hiển thị các nút chức năng của bác sĩ

        # Cập nhật danh sách bác sĩ
            display_doctors(doctor_controller_instance.get_all_doctors())

        elif section == 'treatment':
        # Hiển thị phần điều trị
            treatment_input_frame.pack(side="left", padx=10, pady=5, fill="y")
            treatment_search_frame.pack(fill="x", pady=5)
            treatment_table_frame.pack(fill="both", expand=True, pady=5)
            treatment_button_frame.pack(side="left", padx=10, pady=5)  # Hiển thị các nút chức năng của điều trị

        # Cập nhật danh sách điều trị
            display_treatments(treatment_controller_instance.get_all_treatments())

# Điều chỉnh kích thước bảng điều trị cho phù hợp
    def display_treatments(treatments):
        for item in treatment_tree.get_children():
            treatment_tree.delete(item)
        if treatments:
            for treatment in treatments:
                if len(treatment) == 9: 
                    treatment_tree.insert("", "end", values=treatment)
        else:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị.")


    show_section('doctor_info')  # Hiển thị thông tin bác sĩ ban đầu
def validate_id(value):
    """ Kiểm tra xem giá trị nhập vào có phải là số nguyên hợp lệ không. """
    if value == "" or value.isdigit():
        return True
    return False