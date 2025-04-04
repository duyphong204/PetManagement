from models.medicine_warehouse_model import MedicineWarehouseModel  
from tkinter import messagebox

# Xử lý dữ liệu kho thuốc
class ManageMedicineWarehouseController:
    def __init__(self):
        self.medicine_model = MedicineWarehouseModel()  
        # Tạo một đối tượng của MedicineWarehouseModel để làm việc với dữ liệu kho thuốc.

    def get_all_medicines(self):
        return self.medicine_model.get_all_medicines() 
        # Lấy danh sách toàn bộ thuốc trong kho.

    def add_medicine(self, medicine_data):
        # Có thể thêm kiểm tra hợp lệ trước khi thêm thuốc
        self.medicine_model.add_medicine(medicine_data)  
        # Lưu thuốc mới vào database

    def delete_medicine(self, medicine_id):
        self.medicine_model.delete_medicine(medicine_id)  
        # Xóa thuốc theo ID

    def update_medicine(self, medicine_data):
        self.medicine_model.update_medicine(medicine_data)  
        # Cập nhật thông tin thuốc trong kho

    def search_medicines(self, keyword, field):
        return self.medicine_model.search_medicines(keyword, field)  
        # Tìm kiếm thuốc theo tên hoặc các tiêu chí khác

    def delete_all_medicines(self):
        self.medicine_model.delete_all_medicines()  
        # Xóa toàn bộ danh sách thuốc trong kho
