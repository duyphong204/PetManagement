from models.manage_pet_model import PetModel
from tkinter import messagebox

class ManagePetController:
    def __init__(self):
        self.pet_model = PetModel()

    def get_all_pets(self):
        return self.pet_model.get_all_pets()

    def add_pet(self, pet_data):
        return self.pet_model.add_pet(pet_data)

    def delete_pet(self, pet_id):
        return self.pet_model.delete_pet(pet_id)

    def update_pet(self, pet_id, pet_data):
        return self.pet_model.update_pet(pet_id, pet_data)

    def search_pets(self, keyword):
        return self.pet_model.search_pets(keyword)