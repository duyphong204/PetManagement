import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview, Style
from tkcalendar import DateEntry
import datetime
import controllers.billing_payment_controller as billing_controller
 
def open_invoice_content(frame):
     # Khởi tạo đối tượng ManageInvoiceController
     controller = billing_controller.ManageInvoiceController()
 
     # Tiêu đề
     title_label = ctk.CTkLabel(frame, text="Quản lý Hóa đơn", font=("Arial", 18, "bold"), text_color="black")
     title_label.pack(pady=10)
 
     # Frame chính
     content_frame = ctk.CTkFrame(frame)
     content_frame.pack(pady=10, padx=10, fill="both", expand=True)
 
     # Frame bên trái: Ô nhập liệu
     input_frame = ctk.CTkFrame(content_frame, width=300)
     input_frame.pack(side="left", padx=10, pady=5, fill="y")
 
     # Các ô nhập liệu
     entries = {}
     fields = ["ID Chủ sở hữu", "Tổng tiền", "Ngày tạo", "Trạng thái"]
 
     for field in fields:
         ctk.CTkLabel(input_frame, text=f"{field}:", font=("Arial", 12)).pack(pady=5, anchor="w")
         if field == "Ngày tạo":
             date_entry = DateEntry(input_frame, width=25, date_pattern='yyyy-MM-dd')
             date_entry.pack(pady=5, ipady=8, fill="x", padx=5)
             entries[field] = date_entry
         elif field == "Trạng thái":
             status_combobox = ctk.CTkComboBox(input_frame, values=["Chưa thanh toán", "Đã thanh toán"], width=250)
             status_combobox.pack(pady=5, fill="x", padx=5)
             entries[field] = status_combobox
         else:
             entry = ctk.CTkEntry(input_frame, width=250)
             entry.pack(pady=5, fill="x", padx=5)
             entries[field] = entry
 
     # Frame bên phải: Bảng và nút chức năng
     right_frame = ctk.CTkFrame(content_frame)
     right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)
 
     # Thanh tìm kiếm
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
 
     # Bảng hiển thị dữ liệu
     table_frame = ctk.CTkFrame(right_frame)
     table_frame.pack(fill="both", expand=True, pady=5)
 
     style = Style()
     style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
     style.configure("Treeview", font=("Arial", 12))
 
     columns = ("invoice_id", "owner_id", "total_amount", "created_date", "status")
     tree = Treeview(table_frame, columns=columns, show="headings", height=15)
 
     headers = ["ID Hóa đơn", "ID Chủ sở hữu", "Tổng tiền", "Ngày tạo", "Trạng thái"]
     for col, text in zip(columns, headers):
         tree.heading(col, text=text)
         tree.column(col, width=150)
 
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
         entries["ID Chủ sở hữu"].delete(0, "end")
         entries["ID Chủ sở hữu"].insert(0, values[1])
 
         entries["Tổng tiền"].delete(0, "end")
         entries["Tổng tiền"].insert(0, values[2])
 
         entries["Ngày tạo"].set_date(values[3])
 
         entries["Trạng thái"].set(values[4])
 
     # Gắn sự kiện vào bảng
     tree.bind("<<TreeviewSelect>>", on_tree_select)
 
     # Hàm xử lý các hành động (add, update, delete)
     def handle_action(action):
         try:
             ngay_tao = entries["Ngày tạo"].get_date()
             id_chu_so_huu = entries["ID Chủ sở hữu"].get()
             tong_tien = entries["Tổng tiền"].get()
             trang_thai = entries["Trạng thái"].get()
 
             if not ngay_tao:
                 messagebox.showwarning("Cảnh báo", "Ngày tạo không được để trống!")
                 return
             if not id_chu_so_huu:
                 messagebox.showwarning("Cảnh báo", "ID Chủ sở hữu không được để trống!")
                 return
             if not tong_tien:
                 messagebox.showwarning("Cảnh báo", "Tổng tiền không được để trống!")
                 return
             if not trang_thai:
                 messagebox.showwarning("Cảnh báo", "Trạng thái không được để trống!")
                 return
 
             invoice_data = {
                 "id_chu_so_huu": id_chu_so_huu,
                 "tong_tien": tong_tien,
                 "ngay_tao": ngay_tao.strftime('%Y-%m-%d'),
                 "trang_thai": trang_thai
             }
 
             if action == "add":
                 controller.add_invoice(invoice_data)
             elif action == "update":
                 selected_item = tree.selection()
                 if not selected_item:
                     messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn để cập nhật!")
                     return
                 invoice_data["id"] = tree.item(selected_item)['values'][0]
                 controller.update_invoice(invoice_data)
             elif action == "delete":
                 selected_item = tree.selection()
                 if not selected_item:
                     messagebox.showwarning("Cảnh báo", "Vui lòng chọn hóa đơn để xóa!")
                     return
                 controller.delete_invoice(tree.item(selected_item)['values'][0])
 
             display_invoices()
         except Exception as e:
             messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
 
     # Hàm thực hiện tìm kiếm
     def perform_search():
         keyword = search_entry.get().strip()
         start_date = start_date_entry.get_date()
         end_date = end_date_entry.get_date()
 
         conditions = {}
 
         if start_date:
             conditions["ngay_tao >="] = start_date.strftime('%Y-%m-%d')
         if end_date:
             conditions["ngay_tao <="] = end_date.strftime('%Y-%m-%d')
         if keyword:
             conditions["keyword"] = keyword
 
         try:
             invoices = controller.search_invoices(conditions)
             tree.delete(*tree.get_children())
             for invoice in invoices:
                 tree.insert("", "end", values=(
                     invoice["id"],
                     invoice["id_chu_so_huu"],
                     invoice["tong_tien"],
                     invoice["ngay_tao"],
                     invoice["trang_thai"]
                 ))
         except Exception as e:
             messagebox.showerror("Lỗi", f"Lỗi khi tìm kiếm: {str(e)}")
 
     # Hàm hiển thị hóa đơn
     def display_invoices():
         tree.delete(*tree.get_children())
         invoices = controller.get_all_invoices()
         for invoice in invoices:
             tree.insert("", "end", values=invoice)
 
     # Khung chứa các nút
     button_frame = ctk.CTkFrame(right_frame)
     button_frame.pack(fill="x", padx=10, pady=5)
 
     # Tạo các nút
     add_button = ctk.CTkButton(button_frame, text="Add", command=lambda: handle_action("add"), width=120)
     add_button.pack(side="left", padx=5)
 
     update_button = ctk.CTkButton(button_frame, text="Update", command=lambda: handle_action("update"), width=120)
     update_button.pack(side="left", padx=5)
 
     delete_button = ctk.CTkButton(button_frame, text="Delete", command=lambda: handle_action("delete"), width=120)
     delete_button.pack(side="left", padx=5)
 
     search_button = ctk.CTkButton(button_frame, text="Search", command=lambda: perform_search(), width=120)
     search_button.pack(side="left", padx=5)
 
     # Hiển thị dữ liệu ban đầu
     display_invoices()

     