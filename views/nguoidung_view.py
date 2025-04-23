import customtkinter as ctk
from tkinter import messagebox
from tkinter.ttk import Treeview, Style, Combobox
import controllers.nguoidung_controller as nguoidung_controller

def open_manage_user_content(frame):
    user_controller = nguoidung_controller.UserController()

    title_label = ctk.CTkLabel(frame, text="Quản lý Người dùng", font=("Arial", 18, "bold"), text_color="black")
    title_label.pack(pady=10)

    content_frame = ctk.CTkFrame(frame)
    content_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Frame trái: form nhập
    input_frame = ctk.CTkFrame(content_frame, width=200)
    input_frame.pack(side="left", padx=10, pady=5, fill="y")

    entries = {}
    fields = ["Tên đăng nhập", "Mật khẩu", "Email", "Quyền"]

    for field in fields:
        ctk.CTkLabel(input_frame, text=f"{field}:", font=("Arial", 12)).pack(pady=5, anchor="w")
        if field == "Quyền":
            entry = ctk.CTkComboBox(input_frame, values=["admin", "khach_hang", "bac_si", "none"], width=250)
        else:
            entry = ctk.CTkEntry(input_frame, width=250)
        entry.pack(pady=5)
        entries[field] = entry

    # Frame phải: bảng + nút chức năng
    right_frame = ctk.CTkFrame(content_frame)
    right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=5)

    search_frame = ctk.CTkFrame(right_frame)
    search_frame.pack(fill="x", pady=5)
    ctk.CTkLabel(search_frame, text="Tìm kiếm:", font=("Arial", 12)).pack(side="left", padx=5)
    search_entry = ctk.CTkEntry(search_frame, width=200)
    search_entry.pack(side="left", padx=5)

    table_frame = ctk.CTkFrame(right_frame)
    table_frame.pack(fill="both", expand=True, pady=5)

    # Style Treeview
    style = Style()
    style.configure("Treeview.Heading", font=("Arial", 16, "bold"))
    style.configure("Treeview", font=("Arial", 14))

    # Treeview
    columns = ("id", "username", "password", "email", "role")
    tree = Treeview(table_frame, columns=columns, show="headings", height=15, style="Treeview")

    for col, text in zip(columns, ["ID", "Tên đăng nhập", "Mật khẩu", "Email", "Quyền"]):
        tree.heading(col, text=text)

    tree.column("id", width=50)
    tree.column("username", width=150)
    tree.column("password", width=150)
    tree.column("email", width=200)
    tree.column("role", width=100)
    tree.pack(fill="both", expand=True)

    # Chức năng xử lý
    def display_users(users):
        for item in tree.get_children():
            tree.delete(item)
        if users:
            for user in users:
                if len(user) == 5:
                    tree.insert("", "end", values=user)
        else:
            messagebox.showinfo("Thông báo", "Không có dữ liệu để hiển thị.")

    def clear_form():
        for entry in entries.values():
            if isinstance(entry, ctk.CTkComboBox):  
                entry.set("")
            else:
                entry.delete(0, ctk.END)

    def on_tree_select(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])["values"]
            for i, key in enumerate(fields, start=1):
                if key == "Quyền":
                    entries[key].set(item[i])
                else:
                    entries[key].delete(0, ctk.END)
                    entries[key].insert(0, item[i])


    tree.bind("<<TreeviewSelect>>", on_tree_select)

    def search():
        keyword = search_entry.get().strip()
        users = user_controller.search_users(keyword)
        display_users(users)
        if not users and keyword:
            messagebox.showinfo("Thông báo", "Không tìm thấy người dùng.")

    def handle_action(action, success_msg):
        try:
            user_data = {field: entries[field].get() for field in fields}

            if action in ["add", "update"]:
                for field, value in user_data.items():
                    if not value:
                        messagebox.showwarning("Thiếu thông tin", f"Vui lòng nhập {field}.")
                        return

            if action == "add":
                if user_controller.add_user(user_data):
                    messagebox.showinfo("Thành công", success_msg)
            elif action == "update":
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Chọn người dùng", "Vui lòng chọn người dùng để cập nhật.")
                    return
                user_id = tree.item(selected[0])["values"][0]
                if user_controller.update_user(user_id, user_data):
                    messagebox.showinfo("Thành công", success_msg)
            elif action == "delete":
                selected = tree.selection()
                if not selected:
                    messagebox.showwarning("Chọn người dùng", "Vui lòng chọn người dùng để xóa.")
                    return
                user_id = tree.item(selected[0])["values"][0]
                confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa người dùng này không?")
                if confirm and user_controller.delete_user(user_id):
                    messagebox.showinfo("Thành công", success_msg)

            display_users(user_controller.get_all_users())
            clear_form()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi {action}: {e}")

    # Nút chức năng
    ctk.CTkButton(search_frame, text="Tìm", command=search, width=120).pack(side="left", padx=5)
    button_frame = ctk.CTkFrame(right_frame)
    button_frame.pack(fill="x", padx=10, pady=5)
    ctk.CTkButton(button_frame, text="Thêm", command=lambda: handle_action("add", "Thêm người dùng thành công!"), width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Cập nhật", command=lambda: handle_action("update", "Cập nhật người dùng thành công!"), width=120).pack(side="left", padx=5)
    ctk.CTkButton(button_frame, text="Xóa", command=lambda: handle_action("delete", "Xóa người dùng thành công!"), width=120).pack(side="left", padx=5)

    # Tải dữ liệu ban đầu
    try:
        display_users(user_controller.get_all_users())
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi tải dữ liệu: {e}")
