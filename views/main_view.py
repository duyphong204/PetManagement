import tkinter as tk
from tkinter import Frame, Label, Button
from manage_pet import open_manage_pet  # Import hàm từ file quản lý thú cưng

def open_home():
    home_root = tk.Tk() # Tạo cửa sổ mới trong cùng một ứng dụng
    home_root.title("Quản lý Phòng Khám Thú Y")
    home_root.geometry("800x500")  # Kích thước cửa sổ

    # Tạo Sidebar bên trái
    sidebar = tk.Frame(home_root, bg="#2C3E50", width=200, height=500)
    sidebar.pack(side="left", fill="y")

    # Danh sách các chức năng
    buttons = [
        ("🏠 Trang chủ", None),
        ("🐶 Quản lý Thú cưng", open_manage_pet),
        ("📅 Lịch hẹn khám", None),
        ("📊 Báo cáo", None),
        ("⚙️ Cài đặt", None),
        ("📷 Camera", None),
    ]

    # Thêm các nút vào Sidebar
    for btn_text, command in buttons:
        button = tk.Button(
            sidebar, text=btn_text, fg="white", bg="#34495E",
            font=("Arial", 12), relief="flat",
            padx=10, pady=5, anchor="w",
            command=command
        )
        button.pack(fill="x", pady=5)

    # Phần nội dung chính
    main_content = tk.Frame(home_root, bg="white", width=600, height=500)
    main_content.pack(side="right", fill="both", expand=True)

    label = tk.Label(main_content, text="Chào mừng đến với hệ thống!", font=("Arial", 12))
    label.pack(pady=20)

    home_root.mainloop()
