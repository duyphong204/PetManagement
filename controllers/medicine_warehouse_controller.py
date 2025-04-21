from models.medicine_warehouse_model import MedicineWarehouseModel
from tkinter import messagebox

class ManageMedicineWarehouseController:
    def __init__(self):
        self.medicine_model = MedicineWarehouseModel()

    def get_all_medicines(self):
        return self.medicine_model.get_all_medicines()

    def add_medicine(self, medicine_data):
        self.medicine_model.add_medicine(medicine_data)

    def delete_medicine(self, medicine_id):
        self.medicine_model.delete_medicine(medicine_id)

    def update_medicine(self, medicine_data):
        self.medicine_model.update_medicine(medicine_data)

    def search_medicines(self, keyword, field):
        return self.medicine_model.search_medicines(keyword, field)

    def delete_all_medicines(self):
        self.medicine_model.delete_all_medicines()