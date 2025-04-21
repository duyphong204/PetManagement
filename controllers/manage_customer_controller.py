from models.manage_customer_model import CustomerModel  # Change to import CustomerModel
from tkinter import messagebox

# xử lỹ dữ liệu người dùng 
class ManageCustomerController:
    def __init__(self):
        self.customer_model = CustomerModel()  
        # Nó sẽ tạo một đối tượng của CustomerModel để làm việc với dữ liệu khách hàng.

    def get_all_customers(self):
        return self.customer_model.get_all_customers() 
        # Gọi phương thức get_all_customers() từ CustomerModel để lấy danh sách toàn bộ khách hàng.
        # Phương thức này thường được dùng để cập nhật giao diện khi người dùng
        #  muốn xem danh sách khách hàng. 

    def add_customer(self, customer_data):
        # Add additional validation or logic if needed
        self.customer_model.add_customer(customer_data)  # Add customer to the model
        #Nhận dữ liệu khách hàng customer_data từ giao diện.
        # Có thể thêm các kiểm tra hợp lệ (validation) trước khi thêm vào database.
        # Gọi add_customer() từ CustomerModel để lưu dữ liệu mới vào database

    def delete_customer(self, customer_id):
        self.customer_model.delete_customer(customer_id)  # Delete customer by ID
        # Nhận customer_id của khách hàng cần xóa.
        # Gọi delete_customer() từ CustomerModel để xóa khách hàng trong database.
        # Có thể hiển thị hộp thoại xác nhận trước khi xóa.


    def update_customer(self, customer_data):
        self.customer_model.update_customer(customer_data)  # Update customer data

    # Nhận dữ liệu mới từ giao diện.
     # Gọi update_customer() từ CustomerModel để cập nhật thông tin khách hàng trong database.

    def search_customers(self, keyword, field):
        return self.customer_model.search_customers(keyword, field)  # Search customers by a field
    # Nhận từ khóa (keyword) và trường cần tìm (field) từ giao diện.
    # vd: search_customers("Nguyễn", "name") → Tìm khách hàng có tên chứa "Nguyễn"
    
    
    def delete_all_customers(self):
        self.customer_model.delete_all_customers()  # Delete all customers
    