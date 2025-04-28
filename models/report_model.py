# report_model.py: Truy van du lieu tu co so du lieu de tao bao cao
from utils.connect_dtb import connect_db

class ReportModel:
    def __init__(self):
        # Khoi tao ket noi co so du lieu
        self.ketnoi = connect_db()

    def get_total_revenue(self, ngay_batdau=None, ngay_ketthuc=None):
        # Lay tong doanh thu tu bang hoa_don
        if not self.ketnoi or not self.ketnoi.is_connected():
            return None, "Khong the ket noi den co so du lieu!"
        contro = None
        try:
            contro = self.ketnoi.cursor()
            truyvan = "SELECT SUM(tong_tien) FROM hoa_don"
            thamsot = ()
            if ngay_batdau and ngay_ketthuc:
                truyvan += " WHERE ngay_tao BETWEEN %s AND %s"
                thamsot = (ngay_batdau, ngay_ketthuc)
            contro.execute(truyvan, thamsot)
            tong = contro.fetchone()[0] or 0
            contro.close()
            return tong, None
        except Exception as e:
            if contro: contro.close()
            return None, f"Loi truy van: {e}"

    def get_revenue_details(self, ngay_batdau=None, ngay_ketthuc=None):
        # Lay danh sach hoa don tu bang hoa_don
        if not self.ketnoi or not self.ketnoi.is_connected():
            return None, "Khong the ket noi den co so du lieu!"
        contro = None
        try:
            contro = self.ketnoi.cursor()
            truyvan = "SELECT id, ngay_tao, tong_tien, trang_thai FROM hoa_don"
            thamsot = ()
            if ngay_batdau and ngay_ketthuc:
                truyvan += " WHERE ngay_tao BETWEEN %s AND %s"
                thamsot = (ngay_batdau, ngay_ketthuc)
            contro.execute(truyvan, thamsot)
            chitieut = contro.fetchall()
            contro.close()
            return chitieut, None
        except Exception as e:
            if contro: contro.close()
            return None, f"Loi truy van: {e}"

    def get_revenue_by_date(self, ngay_batdau=None, ngay_ketthuc=None):
        # Nhom doanh thu theo ngay de ve bieu do
        if not self.ketnoi or not self.ketnoi.is_connected():
            return None, "Khong the ket noi den co so du lieu!"
        contro = None
        try:
            contro = self.ketnoi.cursor()
            truyvan = "SELECT DATE(ngay_tao), SUM(tong_tien) FROM hoa_don"
            thamsot = ()
            if ngay_batdau and ngay_ketthuc:
                truyvan += " WHERE ngay_tao BETWEEN %s AND %s"
                thamsot = (ngay_batdau, ngay_ketthuc)
            truyvan += " GROUP BY DATE(ngay_tao)"
            contro.execute(truyvan, thamsot)
            dulieu = contro.fetchall()
            contro.close()
            return dulieu, None
        except Exception as e:
            if contro: contro.close()
            return None, f"Loi truy van: {e}"

    def get_appointment_stats(self, ngay_batdau=None, ngay_ketthuc=None):
    # Thong ke so luong lich hen theo trang thai
        if not self.ketnoi or not self.ketnoi.is_connected():
            return None, "Khong the ket noi den co so du lieu!"
        contro = None
        try:
            contro = self.ketnoi.cursor()
            truyvan = "SELECT trang_thai, COUNT(*) FROM lich_hen"
            thamsot = ()
            if ngay_batdau and ngay_ketthuc:
                truyvan += " WHERE ngay_hen BETWEEN %s AND %s"
                thamsot = (ngay_batdau, ngay_ketthuc)
            truyvan += " GROUP BY trang_thai"
            contro.execute(truyvan, thamsot)
            # Sua tu dien de khop voi gia tri co dau trong co so du lieu
            thongke = {"Chờ xác nhận": 0, "Đã xác nhận": 0, "Đã hoàn thành": 0, "Đã hủy": 0}
            for dong in contro.fetchall():
                if dong[0] in thongke:  # Kiem tra neu trang thai ton tai trong tu dien
                    thongke[dong[0]] = dong[1]
            contro.close()
            return thongke, None
        except Exception as e:
            if contro: contro.close()
            return None, f"Loi truy van: {e}"

    def get_appointment_details(self, ngay_batdau=None, ngay_ketthuc=None):
        # Lay danh sach lich hen tu bang lich_hen
        if not self.ketnoi or not self.ketnoi.is_connected():
            return None, "Khong the ket noi den co so du lieu!"
        contro = None
        try:
            contro = self.ketnoi.cursor()
            truyvan = """
                SELECT lh.id, lh.ngay_hen, lh.gio_hen, tc.ten, bs.ho_ten, lh.trang_thai
                FROM lich_hen lh
                JOIN thu_cung tc ON lh.id_thu_cung = tc.id
                JOIN bac_si bs ON lh.id_bac_si = bs.id
            """
            thamsot = ()
            if ngay_batdau and ngay_ketthuc:
                truyvan += " WHERE lh.ngay_hen BETWEEN %s AND %s"
                thamsot = (ngay_batdau, ngay_ketthuc)
            contro.execute(truyvan, thamsot)
            chitieut = contro.fetchall()
            contro.close()
            return chitieut, None
        except Exception as e:
            if contro: contro.close()
            return None, f"Loi truy van: {e}"

    def get_pet_stats(self):
        # Thong ke so luong thu cung theo loai
        if not self.ketnoi or not self.ketnoi.is_connected():
            return None, "Khong the ket noi den co so du lieu!"
        contro = None
        try:
            contro = self.ketnoi.cursor()
            truyvan = "SELECT loai, COUNT(*) FROM thu_cung GROUP BY loai"
            contro.execute(truyvan)
            thongke = contro.fetchall()
            contro.close()
            return thongke, None
        except Exception as e:
            if contro: contro.close()
            return None, f"Loi truy van: {e}"

    def get_pet_details(self):
        # Lay danh sach thu cung tu bang thu_cung
        if not self.ketnoi or not self.ketnoi.is_connected():
            return None, "Khong the ket noi den co so du lieu!"
        contro = None
        try:
            contro = self.ketnoi.cursor()
            truyvan = """
                SELECT tc.ten, tc.loai, tc.tuoi, tc.gioi_tinh, cs.ho_ten
                FROM thu_cung tc
                JOIN chu_so_huu cs ON tc.id_chu_so_huu = cs.id
            """
            contro.execute(truyvan)
            chitieut = contro.fetchall()
            contro.close()
            return chitieut, None
        except Exception as e:
            if contro: contro.close()
            return None, f"Loi truy van: {e}"

    def get_inventory_stats(self):
        # Thong ke tong so luong va so luong thuoc sap het han
        if not self.ketnoi or not self.ketnoi.is_connected():
            return None, "Khong the ket noi den co so du lieu!"
        contro = None
        try:
            contro = self.ketnoi.cursor()
            truyvan = "SELECT SUM(so_luong) FROM kho_thuoc"
            contro.execute(truyvan)
            tongso = contro.fetchone()[0] or 0

            truyvan = """
                SELECT COUNT(*) 
                FROM kho_thuoc 
                WHERE han_su_dung <= DATE_ADD(CURDATE(), INTERVAL 30 DAY)
            """
            contro.execute(truyvan)
            saphethan = contro.fetchone()[0] or 0
            contro.close()
            return (tongso, saphethan), None
        except Exception as e:
            if contro: contro.close()
            return None, f"Loi truy van: {e}"

    def get_inventory_details(self):
        # Lay danh sach thuoc tu bang kho_thuoc
        if not self.ketnoi or not self.ketnoi.is_connected():
            return None, "Khong the ket noi den co so du lieu!"
        contro = None
        try:
            contro = self.ketnoi.cursor()
            truyvan = """
                SELECT t.ten_thuoc, kt.so_luong, kt.ngay_nhap, kt.han_su_dung
                FROM kho_thuoc kt
                JOIN thuoc t ON t.id_kho_thuoc = kt.id
            """
            contro.execute(truyvan)
            chitieut = contro.fetchall()
            contro.close()
            return chitieut, None
        except Exception as e:
            if contro: contro.close()
            return None, f"Loi truy van: {e}"

    def close_connection(self):
        # Dong ket noi co so du lieu
        if self.ketnoi and self.ketnoi.is_connected():
            self.ketnoi.close()