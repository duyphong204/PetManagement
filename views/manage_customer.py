import customtkinter as ctk
from models.manage_customer_model import CustomerModel
from tkinter import messagebox
from tkinter.ttk import Treeview
import controllers.manage_customer_controller as customer_controller



def open_manage_customer_content(frame):
# Khởi tạo Controller
    customer_controller_instance = customer_controller.ManageCustomerController()


# Xóa nội dung các ô nhập liệu
    def clear_form():
        customer_name_entry.delete(0, ctk.END)
        customer_phone_entry.delete(0, ctk.END)
        customer_email_entry.delete(0, ctk.END)
        customer_address_entry.delete(0, ctk.END)
        user_id_entry.delete(0, ctk.END)


# Tao danh sách khách hàng vào bảng treeview
    def load_customers(customers=None):  
        for item in tree.get_children():
            tree.delete(item)
        if customers is None:
            customers = customer_controller_instance.get_all_customers()
        for customer in customers:
            tree.insert("", "end", values=customer)
            

# Xử lý  thêm khách hàng mới vào hệ thống.
    def add_customer_handler():
        customer_data = {

            "Tên khách hàng": customer_name_entry.get(),
            "Số điện thoại": customer_phone_entry.get(),
            "Email": customer_email_entry.get(),
            "Địa chỉ": customer_address_entry.get(),
            "ID người dùng": user_id_entry.get()
        }
        customer_controller_instance.add_customer(customer_data)
        load_customers()
        clear_form()

# Xử lý xóa khách hàng 
    def delete_customer_handler():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để xóa!")
            return

        customer_id = tree.item(selected_item[0])["values"][0]
        customer_controller_instance.delete_customer(customer_id)
        load_customers()
        clear_form()

# Xử lý cập nhật khách hàng
    def update_customer_handler():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn khách hàng để cập nhật!")
            return

        customer_data = {
            "ID khách hàng": customer_id_entry.get(),
            "Tên khách hàng": customer_name_entry.get(),
            "Số điện thoại": customer_phone_entry.get(),
            "Email": customer_email_entry.get(),
            "Địa chỉ": customer_address_entry.get(),
            "ID người dùng": user_id_entry.get()
        }
        customer_controller_instance.update_customer(customer_data)
        load_customers()
        clear_form()

# Xử lí tìm kiếm khách hàng
    def search_customer_handler():
        search_query = search_entry.get().strip().lower()
        if not search_query:
            load_customers()
            return

        all_customers = customer_controller_instance.get_all_customers()
        filtered_customers = [
            customer for customer in all_customers
            if search_query in str(customer[0]).lower() or
               search_query in str(customer[1]).lower() or
               search_query in str(customer[2]).lower() or
               search_query in str(customer[3]).lower() or
               search_query in str(customer[4]).lower() or
               search_query in str(customer[5]).lower()
        ]
        load_customers(filtered_customers)

# Xử lý sự kiện khi người dùng chọn một dòng trong bảng
    def on_tree_select(event):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item[0])["values"]

            customer_id_entry.delete(0, ctk.END)
            customer_name_entry.delete(0, ctk.END)
            customer_phone_entry.delete(0, ctk.END)
            customer_email_entry.delete(0, ctk.END)
            customer_address_entry.delete(0, ctk.END)
            user_id_entry.delete(0, ctk.END)

            # Đảm bảo số điện thoại được xử lý dưới dạng chuỗi, không mất số 0
            phone_number = str(item[2]).zfill(10)  # Nếu số điện thoại có ít hơn 10 chữ số, sẽ thêm số 0 vào đầu.

            customer_id_entry.insert(0, item[0])
            customer_name_entry.insert(0, item[1])
            customer_phone_entry.insert(0, phone_number)
            customer_email_entry.insert(0, item[3])
            customer_address_entry.insert(0, item[4])
            user_id_entry.insert(0, item[5])
     

#Tiêu đề
    title_label = ctk.CTkLabel(frame, text="Quản lý Khách hàng", font=("Arial", 18, "bold"))
    title_label.pack(pady=10)

#From nhập thông tin khách hàng
    content_frame = ctk.CTkFrame(frame)
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    input_frame = ctk.CTkFrame(content_frame, width=300)
    input_frame.pack(side="left", padx=10, pady=5, fill="y")

    customer_id_entry = ctk.CTkEntry(input_frame, width=250)
    customer_name_entry = ctk.CTkEntry(input_frame, width=250)
    customer_phone_entry = ctk.CTkEntry(input_frame, width=250)
    customer_email_entry = ctk.CTkEntry(input_frame, width=250)
    customer_address_entry = ctk.CTkEntry(input_frame, width=250)
    user_id_entry = ctk.CTkEntry(input_frame, width=250)

    for label, entry in [
       
        ("Tên khách hàng:", customer_name_entry),
        ("Số điện thoại:", customer_phone_entry),
        ("Email:", customer_email_entry),
        ("Địa chỉ:", customer_address_entry),
        ("ID người dùng:", user_id_entry),
    ]:
        ctk.CTkLabel(input_frame, text=label, font=("Arial", 12)).pack(pady=5, anchor="w")
        entry.pack(pady=5)

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


    
#Hiển thị danh sách khách hàng trong bảng.
    table_frame = ctk.CTkFrame(right_frame)
    table_frame.pack(fill="both", expand=True, pady=5)

    columns = ("id", "ho_ten", "so_dien_thoai", "email", "dia_chi", "id_nguoi_dung")
    tree = Treeview(table_frame, columns=columns, show="headings", height=15)

    for col, text, width in [
        ("id", "ID", 30),
        ("ho_ten", "Tên khách hàng", 150),
        ("so_dien_thoai", "Số điện thoại", 120),
        ("email", "Email", 165),
        ("dia_chi", "Địa chỉ", 175),
        ("id_nguoi_dung", "ID Người dùng", 80),
    ]:
        tree.heading(col, text=text)
        tree.column(col, width=width)

    tree.pack(fill="both", expand=True)
    tree.bind("<<TreeviewSelect>>", on_tree_select)
    
# Frame cho các nút chức năng 
    button_frame = ctk.CTkFrame(right_frame)
    button_frame.pack(fill="x", padx=10, pady=5)


#Các nút điều khiển
    add_button = ctk.CTkButton(button_frame, text="Add Customer", command=add_customer_handler, width=120)
    add_button.pack(side="left", padx=5)

    update_button = ctk.CTkButton(button_frame, text="Update Customer", command=update_customer_handler, width=120)
    update_button.pack(side="left", padx=5)

    delete_button = ctk.CTkButton(button_frame, text="Delete Customer", command=delete_customer_handler, width=120)
    delete_button.pack(side="left", padx=5)

    search_button = ctk.CTkButton(button_frame, text="Search", command=search_customer_handler)
    search_button.pack(side="left", padx=5)

    load_customers()