from models.user_model import UserModel

class UserController:
    
    def __init__(self, db_config):
        self.user_model = UserModel(db_config)  # Kết nối UserModel

    def get_user_info(self, user_id):
        """Lấy thông tin cá nhân của người dùng dựa trên user_id"""
        return self.user_model.get_user_info(user_id)
    
    def get_appointments_info(self, user_id):
        """Lấy thông tin các cuộc hẹn của người dùng dựa trên user_id"""
        return self.user_model.get_appointments_info(user_id)

    def show_user_info(self, frame, user_id):
        """Lấy dữ liệu người dùng từ model và truyền cho view."""
        from views.user_view import show_user_info_content, show_error_message  # Import động trong hàm
        user_info = self.get_user_info(user_id)  # Lấy dữ liệu từ model
        if user_info:
            # Gọi view để hiển thị thông tin người dùng
            show_user_info_content(frame, user_info)  # Truyền dữ liệu cho view
        else:
            # Nếu không có dữ liệu, hiển thị thông báo lỗi
            show_error_message(frame)
   
    def show_appointment_content(self, frame, user_id):
        """Lấy thông tin cuộc hẹn của người dùng và gọi view để hiển thị"""
        from views.user_view import show_appointment_content, show_error_message 
        appointments = self.get_appointments_info(user_id)  # Lấy cuộc hẹn từ model
        if appointments:
            show_appointment_content(frame, appointments)  # Truyền dữ liệu cuộc hẹn cho view
        else:
            show_error_message(frame)  # Hiển thị thông báo lỗi nếu không có cuộc hẹn