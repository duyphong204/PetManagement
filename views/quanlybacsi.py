import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from tkinter import messagebox

ctk.set_appearance_mode("Light")  
ctk.set_default_color_theme("blue")
root = ctk.CTk()
root.title("Quản lý Bác Sĩ")
root.geometry("950x650")

frame_left = ctk.CTkFrame(root, width=200, height=200)
frame_left.pack(side="left", fill="y", padx=20, pady=10)
frame_left.pack_propagate(False) 


lbl_title = ctk.CTkLabel(frame_left, text=" Quản lý bác sĩ", font=("Arial", 20, "bold"),wraplength=200)
lbl_title.pack(pady=20 )


btn_info = ctk.CTkButton(frame_left, text=" Thông tin bác sĩ", font=("Arial", 14, "bold"), width=150, height=50,border_width=2, border_color="#006241")
btn_info.pack(pady=20)

btn_shift = ctk.CTkButton(frame_left, text=" Ca trực", font=("Arial", 14, "bold"), width=150, height=50,border_width=2, border_color="#006241")
btn_shift.pack(pady=20 )

btn_schedule = ctk.CTkButton(frame_left, text="Lịch hẹn", font=("Arial", 14, "bold"), width=150, height=50,border_width=2, border_color="#006241")
btn_schedule.pack(pady=20 )

btn_info = ctk.CTkButton(frame_left, text=" Hồ sơ bệnh án", font=("Arial", 14, "bold"), width=150, height=50,border_width=2, border_color="#006241")
btn_info.pack(pady=20)

btn_exit = ctk.CTkButton(frame_left, text="Thoát", fg_color="red", font=("Arial", 14, "bold"), hover_color="darkred", width=150, height=50,border_width=2, border_color="#006241", command=root.quit)
btn_exit.pack(pady=20)

# label hiển thị tên người đăng nhập
lbl_user = ctk.CTkLabel(frame_left, text="(Admin đăng nhập:Nguyễn Văn A)", font=("Arial", 14, "bold"), wraplength=200)
lbl_user.pack(side="bottom", pady=20,padx=5)

frame_right = ctk.CTkFrame(root)
frame_right.pack(side="top", expand=True, fill="both", padx=15, pady=15)
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 14,"bold"))
style.configure("Treeview", font=("Arial", 13)) 
 
columns = ("ID", "Họ tên", "Chuyên môn", "SĐT", "Email")
tree = ttk.Treeview(frame_right, columns=columns, show="headings", height=10)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

tree.pack(expand=True, fill="both", padx=15, pady=10)


frame_bottom = ctk.CTkFrame(root)
frame_bottom.pack(side="bottom", fill="x", padx=15, pady=10)

ctk.CTkLabel(frame_bottom, text="ID:", font=("Arial", 15)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_id = ctk.CTkEntry(frame_bottom, width=150)
entry_id.grid(row=0, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_bottom, text="Họ Tên:", font=("Arial", 15)).grid(row=0, column=2, padx=5, pady=5, sticky="w")
entry_name = ctk.CTkEntry(frame_bottom, width=150)
entry_name.grid(row=0, column=3, padx=5, pady=5)

ctk.CTkLabel(frame_bottom, text="Chuyên môn:", font=("Arial", 15)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_specialty = ctk.CTkEntry(frame_bottom, width=150)
entry_specialty.grid(row=1, column=1, padx=5, pady=5)

ctk.CTkLabel(frame_bottom, text="SĐT:", font=("Arial", 15)).grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_phone = ctk.CTkEntry(frame_bottom, width=150)
entry_phone.grid(row=1, column=3, padx=5, pady=5)

ctk.CTkLabel(frame_bottom, text="Email:", font=("Arial", 15)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_email = ctk.CTkEntry(frame_bottom, width=150)
entry_email.grid(row=2, column=1, padx=5, pady=5)

# Chức năng thêm, sửa, xóa 

def add_doctor():
    new_id = entry_id.get().strip()
    new_name = entry_name.get().strip()
    new_specialty = entry_specialty.get().strip()
    new_phone = entry_phone.get().strip()
    new_email = entry_email.get().strip()

  
    if not new_id or not new_name or not new_specialty or not new_phone or not new_email:
        messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin")
        return

   
    if not new_id.isdigit():
        messagebox.showerror("Lỗi", "ID chỉ được nhập số")
        return

    for child in tree.get_children():
        existing_id = tree.item(child)["values"][0]
        if str(existing_id) == new_id:
            messagebox.showerror("Lỗi", "ID đã tồn tại, vui lòng nhập ID khác")
            return

    
    if not new_name.replace(" ", "").isalpha():
        messagebox.showerror("Lỗi", "Họ tên chỉ được chứa chữ cái")
        return

    if not new_phone.isdigit():
        messagebox.showerror("Lỗi", "Số điện thoại chỉ được chứa số!")
        return

    
    if not (8 <= len(new_phone) <= 13):
        messagebox.showerror("Lỗi", "Số điện thoại phải có từ 8 đến 13 chữ số!")
        return
    
    if "@" not in new_email or "." not in new_email:
        messagebox.showerror("Lỗi", "Email không hợp lệ")
        return

    # Đổi màu xen kẽ cho các dòng
    items = tree.get_children()
    row_color = "even" if len(items) % 2 == 0 else "odd"
    
    tree.insert("", "end", values=(new_id, new_name, new_specialty, new_phone, new_email), tags=(row_color,))
    tree.tag_configure("even", background="#E8E8E8")
    tree.tag_configure("odd", background="white")
    clear_entries()

def edit_doctor():
    selected_item = tree.selection()
    if selected_item:
        tree.item(selected_item, values=(entry_id.get(), entry_name.get(), entry_specialty.get(), entry_phone.get(), entry_email.get()))
        clear_entries()

def delete_doctor():
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item)

def clear_entries():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_specialty.delete(0, tk.END)
    entry_phone.delete(0, tk.END)
    entry_email.delete(0, tk.END)


btn_add = ctk.CTkButton(frame_bottom, text="➕ Thêm", fg_color="green", font=("Arial", 13, "bold"),hover_color="darkgreen",border_width=2, border_color="#006241", command=add_doctor)
btn_add.grid(row=0, column=4, padx=10, pady=10)

btn_edit = ctk.CTkButton(frame_bottom, text="✏️ Sửa", fg_color="darkcyan",font=("Arial", 13, "bold"), hover_color="teal",border_width=2, border_color="#006241", command=edit_doctor)
btn_edit.grid(row=1, column=4, padx=10, pady=10)

btn_delete = ctk.CTkButton(frame_bottom, text="❌ Xóa", fg_color="#DF0029",font=("Arial", 13, "bold"), hover_color="darkred",border_width=2, border_color="#8B0016", command=delete_doctor)
btn_delete.grid(row=2, column=4, padx=10, pady=10)

root.mainloop()
