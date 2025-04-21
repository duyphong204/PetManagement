import customtkinter as ctk
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry  # Thư viện để tạo widget lịch

def create_frame(parent, fg_color="transparent", **kwargs):
    pack_kwargs = {key: kwargs.pop(key) for key in list(kwargs.keys()) if key in ["fill", "padx", "pady", "side", "expand"]}
    frame = ctk.CTkFrame(parent, fg_color=fg_color, **kwargs)
    frame.pack(**pack_kwargs)
    return frame

def create_label(parent, text, font, text_color, **kwargs):
    pack_kwargs = {key: kwargs.pop(key) for key in list(kwargs.keys()) if key in ["fill", "padx", "pady", "side", "expand"]}
    label = ctk.CTkLabel(parent, text=text, font=font, text_color=text_color, **kwargs)
    label.pack(**pack_kwargs)
    return label

def create_button(parent, text, fg_color, hover_color, command, **kwargs):
    pack_kwargs = {key: kwargs.pop(key) for key in list(kwargs.keys()) if key in ["fill", "padx", "pady", "side", "expand"]}
    button = ctk.CTkButton(parent, text=text, font=("Arial", 14, "bold"), fg_color=fg_color,
                           hover_color=hover_color, corner_radius=8, width=150, height=40, command=command, **kwargs)
    button.pack(**pack_kwargs)
    return button

def setup_treeview(table_frame):
    scroll_y = ctk.CTkScrollbar(table_frame, orientation="vertical")
    scroll_y.pack(side="right", fill="y")
    
    tree = ttk.Treeview(table_frame, height=20, yscrollcommand=scroll_y.set)
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    scroll_y.configure(command=tree.yview)
    
    tree["columns"] = ("Danh mục", "Chi tiết", "Giá trị", "Thời gian", "Ghi chú")
    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Danh mục", anchor="w", width=200)
    tree.column("Chi tiết", anchor="w", width=200)
    tree.column("Giá trị", anchor="center", width=100)
    tree.column("Thời gian", anchor="center", width=100)
    tree.column("Ghi chú", anchor="w", width=150)
    tree.heading("Danh mục", text="Danh mục", anchor="w")
    tree.heading("Chi tiết", text="Chi tiết", anchor="w")
    tree.heading("Giá trị", text="Giá trị", anchor="center")
    tree.heading("Thời gian", text="Thời gian", anchor="center")
    tree.heading("Ghi chú", text="Ghi chú", anchor="w")
    
    style = ttk.Style()
    style.configure("Treeview", background="#F5F6F5", foreground="#000000", fieldbackground="#F5F6F5", font=("Arial", 12))
    style.configure("Treeview.Heading", background="#3498DB", foreground="#000000", font=("Arial", 14, "bold"))
    style.map("Treeview", background=[("selected", "#AED6F1")], foreground=[("selected", "#000000")])
    style.map("Treeview.Heading", background=[("active", "#2980B9")])
    tree.tag_configure("oddrow", background="#FFFFFF")
    tree.tag_configure("evenrow", background="#ECF0F1")
    tree.tag_configure("highlight", background="#FFDDC1")
    tree.tag_configure("heading", background="#D5E8D4", font=("Arial", 14, "bold"))
    return tree

def add_data_to_tree(tree, category, detail, value, time="", note="", index=0, highlight=False, is_heading=False):
    tag = "highlight" if highlight else ("heading" if is_heading else ("evenrow" if index % 2 == 0 else "oddrow"))
    tree.insert("", "end", text="", values=(category, detail, value, time, note), tags=(tag,))

def parse_date(date_str):
    """Chuyển đổi chuỗi ngày thành đối tượng datetime."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

def filter_data_by_date_range(data, start_date, end_date):
    """Lọc dữ liệu theo khoảng thời gian từ start_date đến end_date."""
    filtered_data = {}
    start = parse_date(start_date) if start_date else None
    end = parse_date(end_date) if end_date else None

    for key, value in data.items():
        if key in ["Thú cưng theo ngày", "Lịch hẹn theo thời gian", "Doanh thu theo tháng"]:
            filtered_data[key] = []
            if isinstance(value, list):
                for item in value:
                    if "month" in item and "year" in item:
                        day = item.get("day", "01")
                        item_date_str = f"{item['year']}-{item['month']}-{day}"
                        item_date = parse_date(item_date_str)
                        if item_date and (not start or item_date >= start) and (not end or item_date <= end):
                            filtered_data[key].append(item)
                    else:
                        print(f"Warning: Item in {key} is missing 'month' or 'year': {item}")
            elif isinstance(value, dict) and "Theo tháng" in value:
                filtered_data[key] = {"Theo tháng": []}
                for item in value["Theo tháng"]:
                    if "month" in item and "year" in item:
                        day = item.get("day", "01")
                        item_date_str = f"{item['year']}-{item['month']}-{day}"
                        item_date = parse_date(item_date_str)
                        if item_date and (not start or item_date >= start) and (not end or item_date <= end):
                            filtered_data[key]["Theo tháng"].append(item)
                    else:
                        print(f"Warning: Item in {key}['Theo tháng'] is missing 'month' or 'year': {item}")
        else:
            filtered_data[key] = value
    return filtered_data

def display_group(tree, group_name, data, detail_key, value_key, time_keys=None, index_start=0, highlight_condition=None):
    """Hàm tiện ích để hiển thị một nhóm dữ liệu trong Treeview."""
    index = index_start
    if data:
        add_data_to_tree(tree, group_name, "", "", "", "", index, is_heading=True)
        index += 1
        for item in data:
            detail = item.get(detail_key, "N/A")
            value = item.get(value_key, "0")
            time = ""
            if time_keys and all(key in item for key in time_keys):
                day = item.get(time_keys[0], "01")
                month = item[time_keys[1]]
                year = item[time_keys[2]]
                time = f"{year}-{month}-{day}"
            note = "Tháng có doanh thu cao nhất" if highlight_condition and highlight_condition(item) else ""
            highlight = bool(note)
            add_data_to_tree(tree, group_name, detail, value, time, note, index, highlight=highlight)
            index += 1
    return index

def show_report_content(root, report_data):
    from .main_view import create_home_window
    """Hiển thị giao diện báo cáo thống kê với 1 bảng Treeview lớn."""
    for widget in root.winfo_children():
        widget.destroy()

    create_label(root, "Báo cáo thống kê", ("Arial", 24, "bold"), "#2C3E50", pady=15)

    # Thêm bộ lọc với widget lịch
    filter_frame = create_frame(root, fill="x", padx=20, pady=5)
    create_label(filter_frame, "Từ ngày:", ("Arial", 14), "#2C3E50", side="left", padx=5)
    start_date_picker = DateEntry(filter_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    start_date_picker.pack(side="left", padx=5)
    create_label(filter_frame, "Đến ngày:", ("Arial", 14), "#2C3E50", side="left", padx=5)
    end_date_picker = DateEntry(filter_frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    end_date_picker.pack(side="left", padx=5)

    # Tạo frame chính để chứa các bảng và các widget khác
    main_content_frame = create_frame(root, fill="both", expand=True)

    def refresh_tables():
        """Cập nhật lại bảng dữ liệu sau khi lọc."""
        start_date = start_date_picker.get()
        end_date = end_date_picker.get()
        filtered_data = filter_data_by_date_range(report_data, start_date, end_date)

        # Debugging: In dữ liệu đã lọc để kiểm tra
        print("Filtered data:", filtered_data)

        # Xóa dữ liệu cũ trong bảng
        for item in tree.get_children():
            tree.delete(item)

        # Hiển thị dữ liệu trong bảng Treeview
        index = 0
        summary_data = {k: v for k, v in filtered_data.items() if k not in ["Thú cưng theo ngày", "Lịch hẹn theo thời gian", "Doanh thu theo tháng"]}

        # Nhóm: Thú cưng theo loại
        index = display_group(tree, "Thú cưng theo loại", summary_data.get("Thú cưng theo loại", []),
                              "loai", "count", index_start=index)

        # Nhóm: Thú cưng của chủ
        index = display_group(tree, "Thú cưng của chủ", summary_data.get("Thú cưng của chủ", []),
                              "owner_name", "pet_count", index_start=index)

        # Nhóm: Bác sĩ
        index = display_group(tree, "Bác sĩ", summary_data.get("Bác sĩ", []),
                              "ho_ten", "chuyen_mon", index_start=index)

        # Nhóm: Lịch hẹn của bác sĩ
        index = display_group(tree, "Lịch hẹn của bác sĩ", summary_data.get("Lịch hẹn của bác sĩ", []),
                              "ho_ten", "treatment_count", index_start=index)

        # Nhóm: Thuốc
        index = display_group(tree, "Thuốc", summary_data.get("Thuốc", []),
                              "ten_thuoc", "so_luong", index_start=index)

        # Nhóm: Tổng quan
        for key, value in summary_data.items():
            if key not in ["Thú cưng theo loại", "Thú cưng của chủ", "Bác sĩ", "Lịch hẹn của bác sĩ", "Thuốc"]:
                add_data_to_tree(tree, "Tổng quan", "", "", "", "", index, is_heading=True)
                index += 1
                add_data_to_tree(tree, "Tổng quan", key, value, "", "", index)
                index += 1
                break

        # Nhóm: Thú cưng theo ngày
        index = display_group(tree, "Thú cưng theo ngày", filtered_data.get("Thú cưng theo ngày", []),
                              "loai", "count", time_keys=("day", "month", "year"), index_start=index)

        # Nhóm: Lịch hẹn theo thời gian
        index = display_group(tree, "Lịch hẹn theo thời gian", filtered_data.get("Lịch hẹn theo thời gian", {}).get("Theo tháng", []),
                              "trang_thai", "count", time_keys=("day", "month", "year"), index_start=index)

        # Nhóm: Doanh thu theo tháng
        revenue_by_month = filtered_data.get("Doanh thu theo tháng", [])
        max_revenue = max([item['total_revenue'] for item in revenue_by_month], default=0) if revenue_by_month else 0
        index = display_group(tree, "Doanh thu theo tháng", revenue_by_month,
                              "month", "total_revenue", time_keys=("day", "month", "year"), index_start=index,
                              highlight_condition=lambda item: item['total_revenue'] == max_revenue)

        # Cập nhật ô tổng doanh thu
        total_revenue = sum(item['total_revenue'] for item in revenue_by_month)
        for widget in revenue_frame.winfo_children():
            widget.destroy()
        create_label(revenue_frame, "Tổng doanh thu", ("Arial", 14), "white", pady=5)
        create_label(revenue_frame, f"{total_revenue:,} VND", ("Arial", 24, "bold"), "white", pady=5)

    create_button(filter_frame, "Lọc", "#3498DB", "#2980B9", refresh_tables, side="left", padx=5)

    overview_frame = create_frame(main_content_frame, fill="x", padx=20, pady=10)
    
    # Ô tổng quan: Tổng số thú cưng
    pet_frame = create_frame(overview_frame, fg_color="#2ECC71", corner_radius=10, side="left", padx=5)
    create_label(pet_frame, "Tổng số thú cưng", ("Arial", 14), "white", pady=5)
    create_label(pet_frame, str(report_data.get("Tổng số thú cưng", 0)), ("Arial", 24, "bold"), "white", pady=5)

    # Ô tổng quan: Tổng số lịch hẹn
    appt_frame = create_frame(overview_frame, fg_color="#3498DB", corner_radius=10, side="left", padx=5)
    create_label(appt_frame, "Tổng số lịch hẹn", ("Arial", 14), "white", pady=5)
    create_label(appt_frame, str(report_data.get("Tổng số lịch hẹn", 0)), ("Arial", 24, "bold"), "white", pady=5)

    # Ô tổng quan: Doanh thu (tổng)
    revenue_frame = create_frame(overview_frame, fg_color="#E74C3C", corner_radius=10, side="left", padx=5)
    total_revenue = sum(item['total_revenue'] for item in report_data.get("Doanh thu theo tháng", []))
    create_label(revenue_frame, "Tổng doanh thu", ("Arial", 14), "white", pady=5)
    create_label(revenue_frame, f"{total_revenue:,} VND", ("Arial", 24, "bold"), "white", pady=5)

    # Một bảng Treeview lớn
    table_frame = create_frame(main_content_frame, fill="both", expand=True, padx=20, pady=10)
    tree = setup_treeview(table_frame)

    # Hiển thị dữ liệu ban đầu
    refresh_tables()

    button_frame = create_frame(main_content_frame, pady=10)
    create_button(button_frame, "Quay lại", "#E74C3C", "#C0392B", lambda: create_home_window(root), side="left", padx=10)