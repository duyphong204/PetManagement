import mysql.connector
def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="qlthucung"
    )
    print("Kết nối MySQL thành công!")
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")

    print("Danh sách bảng trong CSDL:")
    for (table_name,) in cursor:
        print(f"- {table_name}")

    cursor.close()
    return conn

# # Chạy thử
# if __name__ == "__main__":
#     connect_db()
