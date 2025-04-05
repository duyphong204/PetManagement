from models.quanlybacsi_dieutri_model import TreatmentModel
from datetime import datetime
class TreatmentController:
    def __init__(self):
        self.treatment_model = TreatmentModel()

    def get_all_treatments(self):
        """ Lấy tất cả các bản ghi điều trị """
        return self.treatment_model.get_all_treatments()

    def add_treatment(self, treatment_data):
        """ Thêm điều trị mới vào CSDL """
        self.validate_date(treatment_data["Ngày điều trị"])
        return self.treatment_model.add_treatment(treatment_data)

    def delete_treatment(self, treatment_id):
        """ Xóa điều trị theo ID """
        return self.treatment_model.delete_treatment(treatment_id)

    def update_treatment(self, treatment_id, treatment_data):
        """ Cập nhật thông tin điều trị """
        self.validate_date(treatment_data["Ngày điều trị"])
        return self.treatment_model.update_treatment(treatment_id, treatment_data)

    def search_treatments(self, keyword):
        """ Tìm kiếm điều trị theo từ khóa """
        return self.treatment_model.search_treatments(keyword)

    def get_next_available_id(self):
        """ Lấy ID tiếp theo chưa sử dụng trong bảng dieu_tri """
        return self.treatment_model.get_next_available_id()

    def validate_date(self, date):
        """ Kiểm tra ngày theo định dạng yyyy-mm-dd """
        datetime.strptime(date, "%Y-%m-%d")  # Chỉ kiểm tra ngày, không xử lý lỗi
