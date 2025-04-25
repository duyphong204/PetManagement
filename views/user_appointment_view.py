import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk
from controllers.user_controller import UserController
from datetime import datetime
from tkcalendar import DateEntry

def open_user_appointment_content(frame, user_id, connect_db):
    controller = UserController()

    ctk.CTkLabel(frame, text="Đặt lịch khám", font=("Arial", 20, "bold")).pack(pady=10)

    main_frame = ctk.CTkFrame(frame)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ========== KHUNG TRÁI: Form nhập ==========
    left_frame = ctk.CTkFrame(main_frame, width=300)
    left_frame.pack(side="left", fill="y", padx=10, pady=10)

  # Ngày hẹn
    ctk.CTkLabel(left_frame, text="Chọn ngày hẹn:", anchor="w").pack(pady=5, fill="x")
    date_entry = DateEntry(left_frame, width=17, date_pattern="yyyy-mm-dd")
    date_entry.pack(pady=5)

# Giờ hẹn 
    ctk.CTkLabel(left_frame, text="Giờ hẹn:", anchor="w").pack(pady=5, fill="x")
    gio_values = [f"{h:02d}" for h in range(7, 18)]
    phut_values = [f"{i:02}" for i in range(0, 60, 15)]

 # Tạo frame ngang cho giờ và phút
    time_frame = ctk.CTkFrame(left_frame)
    time_frame.pack(pady=2)

    gio_combobox = ctk.CTkComboBox(time_frame, values=gio_values, width=100)
    gio_combobox.set("Giờ")
    gio_combobox.pack(side="left", padx=5)

    phut_combobox = ctk.CTkComboBox(time_frame, values=phut_values, width=100)
    phut_combobox.set("Phút")
    phut_combobox.pack(side="left", padx=5)

  # Lấy dữ liệu thú cưng và bác sĩ   
    ds_thu_cung = controller.get_pets_by_user(user_id)
    ds_bac_si = controller.get_doctors()
    
    # Chọn thú cưng
    ctk.CTkLabel(left_frame, text="Chọn thú cưng:", anchor="w").pack(pady=5, fill="x")
    pet_combobox = ctk.CTkComboBox(left_frame,
        values=[f"{pet['id']} - {pet['ten']} - {pet['loai']} - {pet['gioi_tinh']}" for pet in ds_thu_cung],
        width=250)
    pet_combobox.pack(pady=5)

   # Chọn bác sĩ
    ctk.CTkLabel(left_frame, text="Chọn bác sĩ:", anchor="w").pack(pady=5, fill="x")
    doctor_combobox = ctk.CTkComboBox(left_frame,
        values=[f"{bs['id']} - {bs['ho_ten']}" for bs in ds_bac_si],
        width=250)
    doctor_combobox.pack(pady=5)

    # ========== KHUNG PHẢI ==========
    right_frame = ctk.CTkFrame(main_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    # ========== KHUNG TÌM KIẾM ==========
    search_frame = ctk.CTkFrame(right_frame)
    search_frame.pack(fill="x", pady=(5, 5))

    ctk.CTkLabel(search_frame, text="Từ ngày:").pack(side="left", padx=5)
    from_date = DateEntry(search_frame, width=12, date_pattern="yyyy-mm-dd")
    from_date.pack(side="left", padx=5)

    ctk.CTkLabel(search_frame, text="Đến ngày:").pack(side="left", padx=5)
    to_date = DateEntry(search_frame, width=12, date_pattern="yyyy-mm-dd")
    to_date.pack(side="left", padx=5)

#Hàm tìm kiếm lịch hẹn của user
    def search_appointments():
        tu_ngay = from_date.get()
        den_ngay = to_date.get()
        if not tu_ngay or not den_ngay:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng chọn cả hai mốc thời gian.")
            return
        try:
            datetime.strptime(tu_ngay, "%Y-%m-%d")
            datetime.strptime(den_ngay, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng ngày không hợp lệ.")
            return
        appointments = controller.search_appointments(user_id, tu_ngay, den_ngay)
        treeview.delete(*treeview.get_children())
        for appt in appointments:
            trang_thai = "Đã xác nhận" if appt["trang_thai"] == "Đã duyệt" else appt["trang_thai"]
            treeview.insert("", "end", values=(
                appt["id"],
                appt["id_thu_cung"],
                appt["id_bac_si"],
                appt["ngay_hen"],
                appt["gio_hen"],
                trang_thai
            ))

#nut tim kiem
    ctk.CTkButton(search_frame, text="Tìm kiếm", command=search_appointments).pack(side="left", padx=10)

    # ========== TREEVIEW ==========
    columns = ("ID", "ID thú cưng", "ID bác sĩ", "Ngày hẹn", "Giờ hẹn", "Trạng thái")
    treeview = ttk.Treeview(right_frame, columns=columns, show="headings", height=15)

    for col in columns:
        treeview.heading(col, text=col)
        treeview.column(col, anchor="center")

    treeview.pack(fill="both", expand=True, pady=(0, 5))

    
   
#tải danh sách lịch hẹn của người dùng và hiển thị lên Treeview 
    def load_appointments():
        appointments = controller.get_appointments_info(user_id)
        treeview.delete(*treeview.get_children())
        for appt in appointments:
            trang_thai = "Đã xác nhận" if appt["trang_thai"] == "Đã duyệt" else appt["trang_thai"]
            treeview.insert("", "end", values=(
                appt["id"],
                appt["id_thu_cung"],
                appt["id_bac_si"],
                appt["ngay_hen"],
                appt["gio_hen"],
                trang_thai
            ))

# hàm xử lý khi người dùng nhấn nút "Đặt lịch" / Đặt lịch mới của user
    def submit_appointment():
        ngay_hen = date_entry.get()
        gio = gio_combobox.get()
        phut = phut_combobox.get()
        gio_hen = f"{gio}:{phut}"

 # Kiểm tra định dạng ngày và giờ
        try:
            datetime.strptime(ngay_hen, "%Y-%m-%d")
            datetime.strptime(gio_hen, "%H:%M")
        except ValueError:
            messagebox.showerror("Lỗi", "Định dạng ngày hoặc giờ không hợp lệ.")
            return

        try:
            id_thu_cung = int(pet_combobox.get().split(" - ")[0])
            id_bac_si = int(doctor_combobox.get().split(" - ")[0])
        except:
            messagebox.showerror("Lỗi", "Vui lòng chọn thú cưng và bác sĩ hợp lệ.")
            return
# Gọi controller để lưu dữ liệu và nhận ID tự động tạo ra
        result = controller.submit_appointment_to_db(ngay_hen, gio_hen, id_thu_cung, id_bac_si)
        if result["success"]:
            messagebox.showinfo("Thành công", result["message"])
            load_appointments()
        else:
            messagebox.showerror("Lỗi", result["message"])

#Ham xoa lich hen user 
    def delete_selected_appointment():
        selected_item = treeview.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một lịch hẹn để xóa.")
            return
        appointment_id = treeview.item(selected_item, "values")[0]
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa lịch hẹn này?"):
            return
        result = controller.delete_appointment(appointment_id)
        if result["success"]:
            messagebox.showinfo("Thành công", result["message"])
            treeview.delete(selected_item)
        else:
            messagebox.showerror("Lỗi", result["message"])

    # ==== Xử lý khi chọn lịch hẹn trong Treeview ====
    def on_treeview_select(event):
     selected_item = treeview.selection()
     if selected_item:
        values = treeview.item(selected_item[0], "values")
        appt_id, pet_id, doctor_id, ngay_hen, gio_hen, _ = values

        # Đặt ngày hẹn
        date_entry.set_date(ngay_hen)

        # Tách giờ và phút từ định dạng HH:MM:SS
        try:
            gio, phut, *_ = gio_hen.split(":")
            gio_combobox.set(gio)
            phut_combobox.set(phut)
        except:
            gio_combobox.set("Giờ")
            phut_combobox.set("Phút")

        # Thiết lập lại chọn thú cưng
        for pet in ds_thu_cung:
            if str(pet["id"]) == str(pet_id):
                pet_combobox.set(f"{pet['id']} - {pet['ten']} - {pet['loai']} - {pet['gioi_tinh']}")
                break

        # Thiết lập lại chọn bác sĩ
        for bs in ds_bac_si:
            if str(bs["id"]) == str(doctor_id):
                doctor_combobox.set(f"{bs['id']} - {bs['ho_ten']}")
                break


    treeview.bind("<<TreeviewSelect>>", on_treeview_select)

    button_frame = ctk.CTkFrame(right_frame)
    button_frame.pack(fill="x", pady=5)

# Nút chức năng
    ctk.CTkButton(button_frame, text="Đặt lịch", command=submit_appointment).pack(side="left", padx=10)
    ctk.CTkButton(button_frame, text="Xóa lịch hẹn", command=delete_selected_appointment).pack(side="left", padx=10)

    load_appointments()
