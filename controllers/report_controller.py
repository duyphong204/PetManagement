# report_controller.py: Dieu khien logic tao bao cao va hien thi giao dien
from datetime import datetime
from models.report_model import ReportModel  
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReportController:
    def __init__(self, khung_giaodien):
        # Khoi tao cac bien co ban
        self.khung_giaodien = khung_giaodien  # Khung giao dien chinh
        self.mohinh = ReportModel()  # Doi tuong de truy van du lieu
        self.nhan_tomtat = None  # Nhan hien thi thong tin tom tat (vi du: tong doanh thu)
        self.khung_bang = None  # Khung chua bang du lieu va bieu do
        self.bieudo = None  # Doi tuong bieu do matplotlib
        self.dulieu_bang = None  # Du lieu hien thi trong bang
        self.tieude_bang = None  # Tieu de cua bang (cac cot)
        self.trang_hientai = 0  # Trang hien tai cua bang (phan trang)
        self.sodong_moitrang = 10  # So dong hien thi tren moi trang

    def generate_report(self, loai_baocao, ngay_batdau, ngay_ketthuc, trang=0):
        # Ham tao bao cao dua tren loai bao cao va khoang thoi gian
        self.trang_hientai = trang  # Cap nhat trang hien tai

        # Kiem tra dinh dang ngay (neu co nhap)
        if ngay_batdau and ngay_ketthuc:
            try:
                datetime.strptime(ngay_batdau, "%Y-%m-%d")
                datetime.strptime(ngay_ketthuc, "%Y-%m-%d")
            except ValueError:
                # Neu dinh dang ngay sai, hien thi thong bao loi
                self.nhan_tomtat.configure(text="Loi: Dinh dang ngay khong hop le (YYYY-MM-DD)!")
                return
        else:
            # Neu khong nhap ngay, de None de lay toan bo du lieu
            ngay_batdau, ngay_ketthuc = None, None

        # Xoa noi dung cu trong khung bang
        for thanhphan in self.khung_bang.winfo_children():
            thanhphan.destroy()
        if self.bieudo:
            # Xoa bieu do cu de tranh ro ri bo nho
            self.bieudo.get_tk_widget().destroy()
            self.bieudo = None

        if loai_baocao == "Doanh thu":
            # Xu ly bao cao Doanh thu
            # 1. Lay tong doanh thu
            tong_doanhthu, loi = self.mohinh.get_total_revenue(ngay_batdau, ngay_ketthuc)
            if loi:
                self.nhan_tomtat.configure(text=loi)
                return
            self.nhan_tomtat.configure(text=f"Tong doanh thu: {tong_doanhthu:,.0f} VND")

            # 2. Lay chi tiet hoa don
            chitieut, loi = self.mohinh.get_revenue_details(ngay_batdau, ngay_ketthuc)
            if loi:
                self.nhan_tomtat.configure(text=loi)
                return
            self.tieude_bang = ["ID", "Ngay tao", "Tong tien", "Trang thai"]
            self.dulieu_bang = [[str(dong[0]), str(dong[1]), f"{dong[2]:,.0f} VND", dong[3]] for dong in chitieut]

            # 3. Ve bieu do: Doanh thu theo ngay
            dulieu, loi = self.mohinh.get_revenue_by_date(ngay_batdau, ngay_ketthuc)
            if loi:
                self.nhan_tomtat.configure(text=loi)
                return
            if dulieu and any(doanhthu for _, doanhthu in dulieu):
                ngay, doanhthu = zip(*dulieu)
                hinh, truc = plt.subplots(figsize=(8, 4))
                truc.bar(ngay, doanhthu, color="#3498DB")
                truc.set_title("Doanh thu theo ngay", fontsize=12, color="#2C3E50")
                truc.set_xlabel("Ngay", fontsize=10)
                truc.set_ylabel("Doanh thu (VND)", fontsize=10)
                plt.xticks(rotation=45, fontsize=8)
                plt.tight_layout()
                self.bieudo = FigureCanvasTkAgg(hinh, master=self.khung_bang)
                self.bieudo.get_tk_widget().grid(row=0, column=0, columnspan=4, pady=10)
            else:
                nhan_khongdulieu = ctk.CTkLabel(self.khung_bang, text="Khong co du lieu de hien thi bieu do",
                                                font=("Arial", 14), text_color="#E74C3C")
                nhan_khongdulieu.grid(row=0, column=0, columnspan=4, pady=10)

        elif loai_baocao == "Lich hen":
            # Xu ly bao cao Lich hen
            # 1. Thong ke trang thai lich hen
            thongke, loi = self.mohinh.get_appointment_stats(ngay_batdau, ngay_ketthuc)
            if loi:
                self.nhan_tomtat.configure(text=loi)
                return
            # Hien thi thong ke voi gia tri tu tu dien moi (co dau)
            self.nhan_tomtat.configure(text=f"Lich hen: Chờ xác nhận: {thongke['Chờ xác nhận']}, "
                                            f"Đã xác nhận: {thongke['Đã xác nhận']}, "
                                            f"Đã hoàn thành: {thongke['Đã hoàn thành']}, "
                                            f"Đã hủy: {thongke['Đã hủy']}")

            # 2. Lay chi tiet lich hen
            chitieut, loi = self.mohinh.get_appointment_details(ngay_batdau, ngay_ketthuc)
            if loi:
                self.nhan_tomtat.configure(text=loi)
                return
            self.tieude_bang = ["ID", "Ngay hen", "Gio hen", "Thu cung", "Bac si", "Trang thai"]
            self.dulieu_bang = [[str(dong[0]), str(dong[1]), str(dong[2]), dong[3], dong[4], dong[5]] for dong in chitieut]

            # 3. Ve bieu do: Ty le trang thai lich hen
            nhan = list(thongke.keys())
            giatri = list(thongke.values())
            if sum(giatri) > 0:
                hinh, truc = plt.subplots(figsize=(6, 4))
                truc.pie(giatri, labels=nhan, autopct='%1.1f%%', colors=["#3498DB", "#E74C3C", "#2ECC71", "#F1C40F"])
                truc.set_title("Ty le trang thai lich hen", fontsize=12, color="#2C3E50")
                plt.tight_layout()
                self.bieudo = FigureCanvasTkAgg(hinh, master=self.khung_bang)
                self.bieudo.get_tk_widget().grid(row=0, column=0, columnspan=6, pady=10)
            else:
                nhan_khongdulieu = ctk.CTkLabel(self.khung_bang, text="Khong co du lieu de hien thi bieu do",
                                                font=("Arial", 14), text_color="#E74C3C")
                nhan_khongdulieu.grid(row=0, column=0, columnspan=6, pady=10)

        elif loai_baocao == "Thu cung":
            # Xu ly bao cao Thu cung
            # 1. Thong ke so luong theo loai
            thongke, loi = self.mohinh.get_pet_stats()
            if loi:
                self.nhan_tomtat.configure(text=loi)
                return
            vanban_thongke = ", ".join([f"{dong[0]}: {dong[1]}" for dong in thongke])
            self.nhan_tomtat.configure(text=f"Thu cung theo loai: {vanban_thongke}")

            # 2. Lay chi tiet thu cung
            chitieut, loi = self.mohinh.get_pet_details()
            if loi:
                self.nhan_tomtat.configure(text=loi)
                return
            self.tieude_bang = ["Ten", "Loai", "Tuoi", "Gioi tinh", "Chu so huu"]
            self.dulieu_bang = [[dong[0], dong[1], str(dong[2]), dong[3], dong[4]] for dong in chitieut]

            # 3. Ve bieu do: So luong thu cung theo loai
            if thongke and any(soluong for _, soluong in thongke):
                loai, soluong = zip(*thongke)
                hinh, truc = plt.subplots(figsize=(7, 4))
                truc.bar(loai, soluong, color="#2ECC71")
                truc.set_title("So luong thu cung theo loai", fontsize=12, color="#2C3E50")
                truc.set_xlabel("Loai", fontsize=10)
                truc.set_ylabel("So luong", fontsize=10)
                plt.xticks(rotation=45, fontsize=8)
                plt.tight_layout()
                self.bieudo = FigureCanvasTkAgg(hinh, master=self.khung_bang)
                self.bieudo.get_tk_widget().grid(row=0, column=0, columnspan=5, pady=10)
            else:
                nhan_khongdulieu = ctk.CTkLabel(self.khung_bang, text="Khong co du lieu de hien thi bieu do",
                                                font=("Arial", 14), text_color="#E74C3C")
                nhan_khongdulieu.grid(row=0, column=0, columnspan=5, pady=10)

        elif loai_baocao == "Kho thuoc":
            # Xu ly bao cao Kho thuoc
            # 1. Thong ke kho
            thongke, loi = self.mohinh.get_inventory_stats()
            if loi:
                self.nhan_tomtat.configure(text=loi)
                return
            tongso, saphethan = thongke
            self.nhan_tomtat.configure(text=f"Tong so luong thuoc: {tongso}, Sap het han: {saphethan}")

            # 2. Lay chi tiet kho thuoc
            chitieut, loi = self.mohinh.get_inventory_details()
            if loi:
                self.nhan_tomtat.configure(text=loi)
                return
            self.tieude_bang = ["Ten thuoc", "So luong", "Ngay nhap", "Han su dung"]
            self.dulieu_bang = [[dong[0], str(dong[1]), str(dong[2]), str(dong[3])] for dong in chitieut]

            # 3. Ve bieu do: Thong ke kho thuoc
            if tongso > 0 or saphethan > 0:
                hinh, truc = plt.subplots(figsize=(6, 4))
                truc.bar(["Tong so luong", "Sap het han"], [tongso, saphethan], color="#F1C40F")
                truc.set_title("Thong ke kho thuoc", fontsize=12, color="#2C3E50")
                truc.set_ylabel("So luong", fontsize=10)
                plt.tight_layout()
                self.bieudo = FigureCanvasTkAgg(hinh, master=self.khung_bang)
                self.bieudo.get_tk_widget().grid(row=0, column=0, columnspan=4, pady=10)
            else:
                nhan_khongdulieu = ctk.CTkLabel(self.khung_bang, text="Khong co du lieu de hien thi bieu do",
                                                font=("Arial", 14), text_color="#E74C3C")
                nhan_khongdulieu.grid(row=0, column=0, columnspan=4, pady=10)

        # Hien thi bang voi phan trang
        chisobatdau = self.trang_hientai * self.sodong_moitrang
        chisoketthuc = chisobatdau + self.sodong_moitrang
        dulieu_phantrang = self.dulieu_bang[chisobatdau:chisoketthuc]

        # Hien thi tieu de bang
        for cot, tieude in enumerate(self.tieude_bang):
            khung_tieude = ctk.CTkFrame(self.khung_bang, fg_color="#34495E", corner_radius=5)
            khung_tieude.grid(row=1, column=cot, padx=2, pady=2, sticky="nsew")
            nhan = ctk.CTkLabel(khung_tieude, text=tieude, font=("Arial", 14, "bold"), text_color="white",
                                width=150, height=30)
            nhan.pack(fill="both", expand=True)

        # Hien thi cac dong du lieu
        for chisodong, dong in enumerate(dulieu_phantrang, start=2):
            maunen = "#ECF0F1" if (chisodong + chisobatdau) % 2 == 0 else "#FFFFFF"
            for chisocot, giatri in enumerate(dong):
                khung_o = ctk.CTkFrame(self.khung_bang, fg_color=maunen, corner_radius=3,
                                       border_width=1, border_color="#D5D8DC")
                khung_o.grid(row=chisodong, column=chisocot, padx=2, pady=2, sticky="nsew")
                nhan = ctk.CTkLabel(khung_o, text=giatri, font=("Arial", 12), text_color="black",
                                    width=150, height=25)
                nhan.pack(fill="both", expand=True)

        # Dieu khien phan trang
        tongsotrang = (len(self.dulieu_bang) + self.sodong_moitrang - 1) // self.sodong_moitrang
        khung_phantrang = ctk.CTkFrame(self.khung_bang, fg_color="white")
        khung_phantrang.grid(row=chisodong + 1, column=0, columnspan=len(self.tieude_bang), pady=10)

        nut_trangtruoc = ctk.CTkButton(khung_phantrang, text="Trang truoc", font=("Arial", 12),
                                       fg_color="#3498DB", hover_color="#2980B9", width=120,
                                       command=lambda: self.generate_report(loai_baocao, ngay_batdau, ngay_ketthuc, self.trang_hientai - 1))
        nut_trangtruoc.pack(side="left", padx=5)
        nut_trangtruoc.configure(state="disabled" if self.trang_hientai == 0 else "normal")

        nhan_trang = ctk.CTkLabel(khung_phantrang, text=f"Trang {self.trang_hientai + 1}/{tongsotrang}",
                                  font=("Arial", 12), text_color="#2C3E50")
        nhan_trang.pack(side="left", padx=5)

        nut_trangsau = ctk.CTkButton(khung_phantrang, text="Trang sau", font=("Arial", 12),
                                     fg_color="#3498DB", hover_color="#2980B9", width=120,
                                     command=lambda: self.generate_report(loai_baocao, ngay_batdau, ngay_ketthuc, self.trang_hientai + 1))
        nut_trangsau.pack(side="left", padx=5)
        nut_trangsau.configure(state="disabled" if self.trang_hientai >= tongsotrang - 1 else "normal")

        for cot in range(len(self.tieude_bang)):
            self.khung_bang.grid_columnconfigure(cot, weight=1)

    def show_report(self):
        # Hien thi giao dien bao cao
        from views.report_view import show_report_content  # Giư nguyen ten ham goc
        show_report_content(self.khung_giaodien, self)

    def close(self):
        # Dong ket noi co so du lieu va xoa bieu do
        self.mohinh.close_connection()
        if self.bieudo:
            self.bieudo.get_tk_widget().destroy()