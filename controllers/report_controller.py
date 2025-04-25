from datetime import datetime
from models.report_model import ReportModel
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReportController:
    def __init__(self, frame):
        self.frame = frame
        self.model = ReportModel()
        self.summary_label = None
        self.table_frame = None
        self.chart_canvas = None
        self.report_data = None
        self.report_headers = None
        self.current_page = 0
        self.rows_per_page = 10

    def generate_report(self, report_type, start_date, end_date, page=0):
        self.current_page = page
        # Validate dates
        if start_date and end_date:
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
                datetime.strptime(end_date, "%Y-%m-%d")
            except ValueError:
                self.summary_label.configure(text="Lỗi: Định dạng ngày không hợp lệ (YYYY-MM-DD)!")
                return
        else:
            start_date, end_date = None, None

        # Clear previous content
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
            self.chart_canvas = None

        if report_type == "Doanh thu":
            # Summary
            total_revenue, error = self.model.get_total_revenue(start_date, end_date)
            if error:
                self.summary_label.configure(text=error)
                return
            self.summary_label.configure(text=f"Tổng doanh thu: {total_revenue:,.0f} VNĐ")

            # Table data
            details, error = self.model.get_revenue_details(start_date, end_date)
            if error:
                self.summary_label.configure(text=error)
                return
            self.report_headers = ["ID", "Ngày tạo", "Tổng tiền", "Trạng thái"]
            self.report_data = [[str(row[0]), str(row[1]), f"{row[2]:,.0f} VNĐ", row[3]] for row in details]

            # Chart: Revenue by date
            data, error = self.model.get_revenue_by_date(start_date, end_date)
            if error:
                self.summary_label.configure(text=error)
                return
            if data and any(revenue for _, revenue in data):
                dates, revenues = zip(*data)
                fig, ax = plt.subplots(figsize=(8, 4))
                ax.bar(dates, revenues, color="#3498DB")
                ax.set_title("Doanh thu theo ngày", fontsize=12, color="#2C3E50")
                ax.set_xlabel("Ngày", fontsize=10)
                ax.set_ylabel("Doanh thu (VNĐ)", fontsize=10)
                plt.xticks(rotation=45, fontsize=8)
                plt.tight_layout()
                self.chart_canvas = FigureCanvasTkAgg(fig, master=self.table_frame)
                self.chart_canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, pady=10)
            else:
                no_data_label = ctk.CTkLabel(self.table_frame, text="Không có dữ liệu để hiển thị biểu đồ",
                                             font=("Arial", 14), text_color="#E74C3C")
                no_data_label.grid(row=0, column=0, columnspan=4, pady=10)

        elif report_type == "Lịch hẹn":
            # Summary
            stats, error = self.model.get_appointment_stats(start_date, end_date)
            if error:
                self.summary_label.configure(text=error)
                return
            self.summary_label.configure(text=f"Lịch hẹn: Chờ xác nhận: {stats['Chờ xác nhận']}, "
                                            f"Đã xác nhận: {stats['Đã xác nhận']}, "
                                            f"Đã hoàn thành: {stats['Đã hoàn thành']}, "
                                            f"Đã hủy: {stats['Đã hủy']}")

            # Table data
            details, error = self.model.get_appointment_details(start_date, end_date)
            if error:
                self.summary_label.configure(text=error)
                return
            self.report_headers = ["ID", "Ngày hẹn", "Giờ hẹn", "Thú cưng", "Bác sĩ", "Trạng thái"]
            self.report_data = [[str(row[0]), str(row[1]), str(row[2]), row[3], row[4], row[5]] for row in details]

            # Chart: Appointment status
            labels = list(stats.keys())
            sizes = list(stats.values())
            if sum(sizes) > 0:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=["#3498DB", "#E74C3C", "#2ECC71", "#F1C40F"])
                ax.set_title("Tỷ lệ trạng thái lịch hẹn", fontsize=12, color="#2C3E50")
                plt.tight_layout()
                self.chart_canvas = FigureCanvasTkAgg(fig, master=self.table_frame)
                self.chart_canvas.get_tk_widget().grid(row=0, column=0, columnspan=6, pady=10)
            else:
                no_data_label = ctk.CTkLabel(self.table_frame, text="Không có dữ liệu để hiển thị biểu đồ",
                                             font=("Arial", 14), text_color="#E74C3C")
                no_data_label.grid(row=0, column=0, columnspan=6, pady=10)

        elif report_type == "Thú cưng":
            # Summary
            stats, error = self.model.get_pet_stats()
            if error:
                self.summary_label.configure(text=error)
                return
            stats_text = ", ".join([f"{row[0]}: {row[1]}" for row in stats])
            self.summary_label.configure(text=f"Thú cưng theo loài: {stats_text}")

            # Table data
            details, error = self.model.get_pet_details()
            if error:
                self.summary_label.configure(text=error)
                return
            self.report_headers = ["Tên", "Loài", "Tuổi", "Giới tính", "Chủ sở hữu"]
            self.report_data = [[row[0], row[1], str(row[2]), row[3], row[4]] for row in details]

            # Chart: Pets by species
            if stats and any(count for _, count in stats):
                species, counts = zip(*stats)
                fig, ax = plt.subplots(figsize=(7, 4))
                ax.bar(species, counts, color="#2ECC71")
                ax.set_title("Số lượng thú cưng theo loài", fontsize=12, color="#2C3E50")
                ax.set_xlabel("Loài", fontsize=10)
                ax.set_ylabel("Số lượng", fontsize=10)
                plt.xticks(rotation=45, fontsize=8)
                plt.tight_layout()
                self.chart_canvas = FigureCanvasTkAgg(fig, master=self.table_frame)
                self.chart_canvas.get_tk_widget().grid(row=0, column=0, columnspan=5, pady=10)
            else:
                no_data_label = ctk.CTkLabel(self.table_frame, text="Không có dữ liệu để hiển thị biểu đồ",
                                             font=("Arial", 14), text_color="#E74C3C")
                no_data_label.grid(row=0, column=0, columnspan=5, pady=10)

        elif report_type == "Kho thuốc":
            # Summary
            stats, error = self.model.get_inventory_stats()
            if error:
                self.summary_label.configure(text=error)
                return
            total, expiring = stats
            self.summary_label.configure(text=f"Tổng số lượng thuốc: {total}, Sắp hết hạn: {expiring}")

            # Table data
            details, error = self.model.get_inventory_details()
            if error:
                self.summary_label.configure(text=error)
                return
            self.report_headers = ["Tên thuốc", "Số lượng", "Ngày nhập", "Hạn sử dụng"]
            self.report_data = [[row[0], str(row[1]), str(row[2]), str(row[3])] for row in details]

            # Chart: Inventory
            if total > 0 or expiring > 0:
                fig, ax = plt.subplots(figsize=(6, 4))
                ax.bar(["Tổng số lượng", "Sắp hết hạn"], [total, expiring], color="#F1C40F")
                ax.set_title("Thống kê kho thuốc", fontsize=12, color="#2C3E50")
                ax.set_ylabel("Số lượng", fontsize=10)
                plt.tight_layout()
                self.chart_canvas = FigureCanvasTkAgg(fig, master=self.table_frame)
                self.chart_canvas.get_tk_widget().grid(row=0, column=0, columnspan=4, pady=10)
            else:
                no_data_label = ctk.CTkLabel(self.table_frame, text="Không có dữ liệu để hiển thị biểu đồ",
                                             font=("Arial", 14), text_color="#E74C3C")
                no_data_label.grid(row=0, column=0, columnspan=4, pady=10)

        # Display table with pagination
        start_idx = self.current_page * self.rows_per_page
        end_idx = start_idx + self.rows_per_page
        paginated_data = self.report_data[start_idx:end_idx]

        # Table headers
        for col, header in enumerate(self.report_headers):
            header_frame = ctk.CTkFrame(self.table_frame, fg_color="#34495E", corner_radius=5)
            header_frame.grid(row=1, column=col, padx=2, pady=2, sticky="nsew")
            label = ctk.CTkLabel(header_frame, text=header, font=("Arial", 14, "bold"), text_color="white",
                                 width=150, height=30)
            label.pack(fill="both", expand=True)

        # Table rows
        for row_idx, row in enumerate(paginated_data, start=2):
            bg_color = "#ECF0F1" if (row_idx + start_idx) % 2 == 0 else "#FFFFFF"
            for col_idx, value in enumerate(row):
                cell_frame = ctk.CTkFrame(self.table_frame, fg_color=bg_color, corner_radius=3,
                                          border_width=1, border_color="#D5D8DC")
                cell_frame.grid(row=row_idx, column=col_idx, padx=2, pady=2, sticky="nsew")
                label = ctk.CTkLabel(cell_frame, text=value, font=("Arial", 12), text_color="black",
                                     width=150, height=25)
                label.pack(fill="both", expand=True)

        # Pagination controls
        total_pages = (len(self.report_data) + self.rows_per_page - 1) // self.rows_per_page
        pagination_frame = ctk.CTkFrame(self.table_frame, fg_color="white")
        pagination_frame.grid(row=row_idx + 1, column=0, columnspan=len(self.report_headers), pady=10)

        prev_button = ctk.CTkButton(pagination_frame, text="Trang trước", font=("Arial", 12),
                                    fg_color="#3498DB", hover_color="#2980B9", width=120,
                                    command=lambda: self.generate_report(report_type, start_date, end_date, self.current_page - 1))
        prev_button.pack(side="left", padx=5)
        prev_button.configure(state="disabled" if self.current_page == 0 else "normal")

        page_label = ctk.CTkLabel(pagination_frame, text=f"Trang {self.current_page + 1}/{total_pages}",
                                  font=("Arial", 12), text_color="#2C3E50")
        page_label.pack(side="left", padx=5)

        next_button = ctk.CTkButton(pagination_frame, text="Trang sau", font=("Arial", 12),
                                    fg_color="#3498DB", hover_color="#2980B9", width=120,
                                    command=lambda: self.generate_report(report_type, start_date, end_date, self.current_page + 1))
        next_button.pack(side="left", padx=5)
        next_button.configure(state="disabled" if self.current_page >= total_pages - 1 else "normal")

        for col in range(len(self.report_headers)):
            self.table_frame.grid_columnconfigure(col, weight=1)

    def show_report(self):
        from views.report_view import show_report_content
        show_report_content(self.frame, self)

    def close(self):
        self.model.close_connection()
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()