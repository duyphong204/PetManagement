# report_view.py: Tao giao dien cho chuc nang bao cao
import customtkinter as ctk
import controllers.report_controller as report_controller

def show_report_content(khung, dieukhien):
    # Xoa noi dung cu trong khung
    for thanhphan in khung.winfo_children():
        thanhphan.destroy()

    # Tao khung chinh
    khung_chinh = ctk.CTkFrame(khung, fg_color="white", corner_radius=15, border_width=2, border_color="#E0E0E0")
    khung_chinh.pack(fill="both", expand=True, padx=20, pady=20)

    # Tieu de
    nhan_tieude = ctk.CTkLabel(khung_chinh, text="BAO CAO THONG KE", font=("Arial", 30, "bold"), text_color="#1F618D")
    nhan_tieude.pack(pady=(20, 25))

    # Khung bo loc
    khung_boloc = ctk.CTkFrame(khung_chinh, fg_color="#F7F9F9", corner_radius=10)
    khung_boloc.pack(fill="x", pady=15, padx=15)

    nhan_loaibaocao = ctk.CTkLabel(khung_boloc, text="Loai bao cao:", font=("Arial", 16, "bold"), text_color="#2C3E50")
    nhan_loaibaocao.pack(side="left", padx=(10, 5))

    hopchon_loaibaocao = ctk.CTkComboBox(khung_boloc, values=["Doanh thu", "Lich hen", "Thu cung", "Kho thuoc"],
                                         font=("Arial", 16), width=160, dropdown_fg_color="#34495E",
                                         dropdown_text_color="white", fg_color="white", text_color="black")
    hopchon_loaibaocao.pack(side="left", padx=10)
    hopchon_loaibaocao.set("Doanh thu")

    nhan_ngaybatdau = ctk.CTkLabel(khung_boloc, text="Tu ngay:", font=("Arial", 16, "bold"), text_color="#2C3E50")
    nhan_ngaybatdau.pack(side="left", padx=(20, 5))
    
    onhap_ngaybatdau = ctk.CTkEntry(khung_boloc, placeholder_text="YYYY-MM-DD", width=130, font=("Arial", 16), fg_color="white")
    onhap_ngaybatdau.pack(side="left", padx=5)
    
    nhan_ngayketthuc = ctk.CTkLabel(khung_boloc, text="Den ngay:", font=("Arial", 16, "bold"), text_color="#2C3E50")
    nhan_ngayketthuc.pack(side="left", padx=5)
    
    onhap_ngayketthuc = ctk.CTkEntry(khung_boloc, placeholder_text="YYYY-MM-DD", width=130, font=("Arial", 16), fg_color="white")
    onhap_ngayketthuc.pack(side="left", padx=5)

    nut_taobaocao = ctk.CTkButton(khung_boloc, text="Tao bao cao", font=("Arial", 16, "bold"),
                                  fg_color="#3498DB", hover_color="#2980B9", width=130,
                                  command=lambda: dieukhien.generate_report(
                                      hopchon_loaibaocao.get(),
                                      onhap_ngaybatdau.get(),
                                      onhap_ngayketthuc.get()))
    nut_taobaocao.pack(side="left", padx=(20, 0))

    # Khung tom tat
    khung_tomtat = ctk.CTkFrame(khung_chinh, fg_color="white")
    khung_tomtat.pack(fill="x", pady=15)

    dieukhien.nhan_tomtat = ctk.CTkLabel(khung_tomtat, text="Tong doanh thu: 0 VND",
                                         font=("Arial", 18, "bold"), text_color="#2C3E50")
    dieukhien.nhan_tomtat.pack(pady=10)

    # Khung bang co the cuon
    khung_cuon = ctk.CTkScrollableFrame(khung_chinh, fg_color="white", corner_radius=10)
    khung_cuon.pack(fill="both", expand=True, padx=15, pady=15)

    dieukhien.khung_bang = ctk.CTkFrame(khung_cuon, fg_color="white")
    dieukhien.khung_bang.pack(fill="both", expand=True)

    dieukhien.generate_report("Doanh thu", "", "")