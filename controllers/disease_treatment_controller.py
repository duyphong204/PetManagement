from models.disease_treatment_model import TreatmentModel
 
class ManageTreatmentController:
     def __init__(self):
         self.treatment_model = TreatmentModel()
 
     def get_all_treatments(self):
         return self.treatment_model.get_all_treatments()
 
     def add_treatment(self, treatment_data):
         self.treatment_model.add_treatment(treatment_data)
 
     def update_treatment(self, treatment_data):
         self.treatment_model.update_treatment(treatment_data)
 
     def delete_treatment(self, treatment_id):
         self.treatment_model.delete_treatment(treatment_id)
 
     def search_treatments(self, conditions):
         return self.treatment_model.search_treatments(conditions)