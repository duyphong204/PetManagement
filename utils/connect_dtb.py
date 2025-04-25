import mysql.connector
from mysql.connector import pooling

class DatabaseConnection:
    _connection_pool = None

    @classmethod
    def initialize(cls):
        """Khởi tạo connection pool."""
        if cls._connection_pool is None:
            cls._connection_pool = pooling.MySQLConnectionPool(
                pool_name="mypool",
                pool_size=5,  # Số kết nối tối đa trong pool
                host="localhost",
                user="root",
                password="",
                database="qlthucung2"
            )
            print("Kết nối MySQL thành công!")  # Chỉ in thông báo này một lần

    @classmethod
    def get_connection(cls):
        """Lấy một kết nối từ pool."""
        if cls._connection_pool is None:
            cls.initialize()
        return cls._connection_pool.get_connection()

def connect_db():
    """Hàm tiện ích để lấy kết nối."""
    return DatabaseConnection.get_connection()

# Chạy thử
if __name__ == "__main__":
    conn = connect_db()
    if conn and conn.is_connected():
        print("Kết nối thử nghiệm thành công!")
        conn.close()