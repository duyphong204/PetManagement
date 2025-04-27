from models.quanlybacsi_model import DoctorModel

class DoctorController:
    def __init__(self):
        self.doctor_model = DoctorModel()

    def get_all_doctors(self):
        return self.doctor_model.get_all_doctors()

    def add_doctor(self, doctor_data):
        return self.doctor_model.add_doctor(doctor_data)

    def update_doctor(self, doctor_id, doctor_data):
        return self.doctor_model.update_doctor(doctor_id, doctor_data)

    def delete_doctor(self, doctor_id):
        return self.doctor_model.delete_doctor(doctor_id)

    def search_doctors(self, keyword):
        return self.doctor_model.search_doctors(keyword)

    def process_id_nguoi_dung(self, id_nguoi_dung):
        return self.doctor_model.process_id_nguoi_dung(id_nguoi_dung)

    def get_next_available_id(self):
        return self.doctor_model.get_next_available_id()