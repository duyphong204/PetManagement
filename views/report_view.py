import customtkinter as ctk

def show_report_content(frame, controller):
    for widget in frame.winfo_children():
        widget.destroy()

    main_frame = ctk.CTkFrame(frame, fg_color="white", corner_radius=15, border_width=2, border_color="#E0E0E0")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Title
    title_label = ctk.CTkLabel(main_frame, text="BÁO CÁO THỐNG KẾ", font=("Arial", 30, "bold"), text_color="#1F618D")
    title_label.pack(pady=(20, 25))

    # Filter frame
    filter_frame = ctk.CTkFrame(main_frame, fg_color="#F7F9F9", corner_radius=10)
    filter_frame.pack(fill="x", pady=15, padx=15)

    report_type_label = ctk.CTkLabel(filter_frame, text="Loại báo cáo:", font=("Arial", 16, "bold"), text_color="#2C3E50")
    report_type_label.pack(side="left", padx=(10, 5))

    report_type_combobox = ctk.CTkComboBox(filter_frame, values=["Doanh thu", "Lịch hẹn", "Thú cưng", "Kho thuốc"],
                                           font=("Arial", 16), width=160, dropdown_fg_color="#34495E",
                                           dropdown_text_color="white", fg_color="white", text_color="black")
    report_type_combobox.pack(side="left", padx=10)
    report_type_combobox.set("Doanh thu")

    start_date_label = ctk.CTkLabel(filter_frame, text="Từ ngày:", font=("Arial", 16, "bold"), text_color="#2C3E50")
    start_date_label.pack(side="left", padx=(20, 5))
    
    start_date_entry = ctk.CTkEntry(filter_frame, placeholder_text="YYYY-MM-DD", width=130, font=("Arial", 16), fg_color="white")
    start_date_entry.pack(side="left", padx=5)
    
    end_date_label = ctk.CTkLabel(filter_frame, text="Đến ngày:", font=("Arial", 16, "bold"), text_color="#2C3E50")
    end_date_label.pack(side="left", padx=5)
    
    end_date_entry = ctk.CTkEntry(filter_frame, placeholder_text="YYYY-MM-DD", width=130, font=("Arial", 16), fg_color="white")
    end_date_entry.pack(side="left", padx=5)

    generate_button = ctk.CTkButton(filter_frame, text="Tạo báo cáo", font=("Arial", 16, "bold"),
                                    fg_color="#3498DB", hover_color="#2980B9", width=130,
                                    command=lambda: controller.generate_report(
                                        report_type_combobox.get(),
                                        start_date_entry.get(),
                                        end_date_entry.get()))
    generate_button.pack(side="left", padx=(20, 0))

    # Summary and Chart frame
    summary_frame = ctk.CTkFrame(main_frame, fg_color="white")
    summary_frame.pack(fill="x", pady=15)

    controller.summary_label = ctk.CTkLabel(summary_frame, text="Tổng doanh thu: 0 VNĐ",
                                            font=("Arial", 18, "bold"), text_color="#2C3E50")
    controller.summary_label.pack(pady=10)

    # Table frame with scrollbar
    scrollable_frame = ctk.CTkScrollableFrame(main_frame, fg_color="white", corner_radius=10)
    scrollable_frame.pack(fill="both", expand=True, padx=15, pady=15)

    controller.table_frame = ctk.CTkFrame(scrollable_frame, fg_color="white")
    controller.table_frame.pack(fill="both", expand=True)

    controller.generate_report("Doanh thu", "", "")