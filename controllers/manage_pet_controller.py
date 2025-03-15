from models.manage_pet_model import PetModel
from tkinter import messagebox

class ManagePetController:
    def __init__(self):
        self.pet_model = PetModel()

    def get_all_pets(self):
        return self.pet_model.get_all_pets()

    def add_pet(self, pet_data):
        # Thêm logic kiểm tra bổ sung nếu cần
        self.pet_model.add_pet(pet_data)

    def delete_pet(self, pet_id):
        self.pet_model.delete_pet(pet_id)

    def update_pet(self, pet_data):
        self.pet_model.update_pet(pet_data)

    def search_pets(self, keyword, field):
        return self.pet_model.search_pets(keyword, field)

    def delete_all_pets(self):
        self.pet_model.delete_all_pets()