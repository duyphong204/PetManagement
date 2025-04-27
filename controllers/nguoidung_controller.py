from models.nguoidung_model import UserModel

class UserController:
    def __init__(self):
        self.user_model = UserModel()

    def get_all_users(self):
        return self.user_model.get_all_users()

    def add_user(self, user_data):
        return self.user_model.add_user(user_data)

    def update_user(self, user_id, user_data):
        return self.user_model.update_user(user_id, user_data)

    def delete_user(self, user_id):  
        return self.user_model.delete_user(user_id)

    def search_users(self, keyword):
        return self.user_model.search_user(keyword) 

    def get_next_available_id(self):
        return self.user_model.get_next_available_id()