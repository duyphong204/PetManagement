from models.KeDon_model import PrescriptionModel

class PrescriptionController:
    def __init__(self):
        self.model = PrescriptionModel()

    def get_appointments(self):
        return self.model.get_appointments()

    def get_medicines(self):
        return self.model.get_medicines()

    def prescribe_medicine(self, prescription_data):
        return self.model.prescribe_medicine(prescription_data)

    def update_prescription(self, prescription_id, prescription_data):
        return self.model.update_prescription(prescription_id, prescription_data)

    def delete_prescription(self, prescription_id):
        return self.model.delete_prescription(prescription_id)

    def search_prescriptions(self, keyword, field):
        return self.model.search_prescriptions(keyword, field)

    def get_all_prescriptions(self):
        return self.model.get_all_prescriptions()