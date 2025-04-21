from models.report_model import ReportModel
import views.report_view as report_view

class ReportController:
    def __init__(self, root):
        self.root = root
        self.model = ReportModel()

    def show_report(self):
        """Hiển thị báo cáo tổng quát."""
        report_data = {
            "Tổng số thú cưng": self.model.get_pet_statistics().get("Tổng số thú cưng", 0),
            "Thú cưng theo loại": self.model.get_pet_statistics().get("Thú cưng theo loại", []),
            "Thú cưng theo ngày": self.model.get_pet_by_date(),
            "Thú cưng theo chủ sở hữu": self.model.get_pet_by_owner(),
            "Tổng số lịch hẹn": self.model.get_appointment_statistics().get("Tổng số lịch hẹn", 0),
            "Lịch hẹn đã xác nhận": self.model.get_appointment_statistics().get("Lịch hẹn đã xác nhận", 0),
            "Lịch hẹn chưa xác nhận": self.model.get_appointment_statistics().get("Lịch hẹn chưa xác nhận", 0),
            "Lịch hẹn theo thời gian": self.model.get_appointment_by_date(),
            "Bác sĩ và chuyên môn": self.model.get_doctor_statistics().get("Bác sĩ và chuyên môn", []),
            "Số ca điều trị theo bác sĩ": self.model.get_doctor_statistics().get("Số ca điều trị theo bác sĩ", []),
            "Doanh thu theo tháng": self.model.get_revenue_statistics(),
            "Tổng số loại thuốc": self.model.get_medicine_statistics().get("Tổng số loại thuốc", 0),
            "Tổng số lượng thuốc": self.model.get_medicine_statistics().get("Tổng số lượng thuốc", 0),
            "Thuốc theo loại": self.model.get_medicine_statistics().get("Thuốc theo loại", []),
            "Thuốc sắp hết hạn": self.model.get_medicine_statistics().get("Thuốc sắp hết hạn", []),
        }
        report_view.show_report_content(self.root, report_data)

    def show_health_report(self):
        """Hiển thị báo cáo sức khỏe thú cưng."""
        report_data = {
            "Tổng số thú cưng": self.model.get_pet_health_statistics().get("Tổng số thú cưng", 0),
            "Thú cưng theo tình trạng sức khỏe": self.model.get_pet_health_statistics().get("Thú cưng theo tình trạng sức khỏe", []),
            "Thú cưng theo tình trạng sức khỏe qua thời gian": self.model.get_pet_health_by_date(),
            "Thú cưng theo tình trạng sức khỏe và loài": self.model.get_pet_health_by_type(),
        }
        report_view.show_health_report_content(self.root, report_data)