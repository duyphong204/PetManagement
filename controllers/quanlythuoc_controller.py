from models.quanlythuoc_model import DrugModel

class DrugController:
    def __init__(self):
        self.model = DrugModel()

    def add_drug(self, drug_data):
        return self.model.add_medicine(drug_data)

    def delete_drug(self, drug_id):
        return self.model.delete_medicine(drug_id)

    def update_drug(self, drug_id, drug_data):
        return self.model.update_medicine(drug_id, drug_data)

    def search_drugs(self, keyword, field):
        return self.model.search_medicine(keyword, field)

    def get_all_drugs(self):
        return self.model.get_all_medicine()