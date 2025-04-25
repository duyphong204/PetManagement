
from models.user_model import UserModel

class UserController:
    def __init__(self):
        self.user_model = UserModel()

    def get_user_info(self, user_id):
        """Lấy thông tin cá nhân của người dùng dựa trên user_id"""
        return self.user_model.get_user_info(user_id)

    def show_user_info(self, frame, user_id):
        """Gọi view để hiển thị thông tin người dùng"""
        from views.user_view import show_user_info_content, show_error_message
        user_info = self.get_user_info(user_id)
        if user_info:
            show_user_info_content(frame, user_info)
        else:
            show_error_message(frame)

    def show_appointment_content(self, frame, user_id):
        """Gọi view để hiển thị thông tin các cuộc hẹn"""
        from views.user_view import show_appointment_content, show_error_message
        appointments = self.get_appointments_info(user_id)
        if appointments:
            show_appointment_content(frame, appointments)
        else:
            show_error_message(frame)

    def get_pets_by_user(self, user_id):
        """Lấy danh sách thú cưng của người dùng"""
        return self.user_model.get_pets_by_user(user_id)

    def get_doctors(self):
        """Lấy danh sách bác sĩ"""
        return self.user_model.get_doctors()
    
    def submit_appointment_to_db(self, ngay_hen, gio_hen, id_thu_cung, id_bac_si):
     """Hàm để đặt lịch hẹn, kiểm tra trùng lịch trước khi lưu."""

    # Kiem tra co trung lich hen khong
     if self.user_model.check_duplicate_appointment(ngay_hen, gio_hen, id_bac_si):
        return {"success": False, "message": "Lịch hẹn đã có vào thời gian này."}

    # Kiểm tra khoảng cách 30 phút
     if not self.user_model.is_time_slot_available(ngay_hen, gio_hen):
        return {"success": False, "message": "Lịch hẹn phải cách các lịch khác ít nhất 30 phút!"}

    # Tiến hành lưu lịch hẹn vào cơ sở dữ liệu
     self.user_model.save_appointment(ngay_hen, gio_hen, id_thu_cung, id_bac_si)
     return {"success": True, "message": "Lịch hẹn đã được đặt thành công!"}


    def get_appointments_info(self, user_id):
        """Lấy danh sách cuộc hẹn của người dùng"""
        return self.user_model.get_appointments_info(user_id)
    
    def delete_appointment(self, appointment_id):
     return self.user_model.delete_appointment(appointment_id)
    
    def search_appointments(self, user_id, tu_ngay, den_ngay):
        return self.user_model.search_appointments(user_id, tu_ngay, den_ngay)