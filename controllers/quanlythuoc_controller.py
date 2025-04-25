from models.quanlythuoc_model import DrugModel

class DrugController:
    def __init__(self):
        self.model = DrugModel()

    def get_medicine_names_by_kho_thuoc_id(self, id_kho_thuoc):
        return self.model.get_medicine_names_by_kho_thuoc_id(id_kho_thuoc)

    def get_drugs_by_kho_thuoc_id(self, id_kho_thuoc):
        return self.model.get_medicine_names_by_kho_thuoc_id(id_kho_thuoc)

    def get_all_drugs(self):
        return self.model.get_all_medicine()

    def get_kho_thuoc_id_by_name(self, ten_thuoc):
        return self.model.get_kho_thuoc_id_by_name(ten_thuoc)

    def add_drug(self, drug_data, kho_thuoc_id=None):
        return self.model.add_medicine(drug_data, kho_thuoc_id)

    def update_drug(self, drug_id, drug_data, kho_thuoc_id=None):
        return self.model.update_medicine(drug_id, drug_data, kho_thuoc_id)

    def delete_drug(self, drug_id):
        return self.model.delete_medicine(drug_id)

    def search_drugs(self, keyword, field):
        return self.model.search_medicine(keyword, field)