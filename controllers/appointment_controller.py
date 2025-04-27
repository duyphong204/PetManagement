from models.appointment_model import AppointmentModel

class ManageAppointmentController:
    def __init__(self):
        self.appointment_model = AppointmentModel()

    def get_all_appointments(self):
        return self.appointment_model.get_all_appointments()

    def add_appointment(self, appointment_data):
        self.appointment_model.add_appointment(appointment_data)

    def update_appointment(self, appointment_data):
        self.appointment_model.update_appointment(appointment_data)

    def delete_appointment(self, appointment_id):
        self.appointment_model.delete_appointment(appointment_id)

    def search_appointments(self, conditions):
        return self.appointment_model.search_appointments(conditions)

    def get_doctors(self):
        return self.appointment_model.get_doctors()

    def get_doctor_id_by_name(self, doctor_name):
        return self.appointment_model.get_doctor_id_by_name(doctor_name)