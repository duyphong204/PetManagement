import mysql.connector

def create_connection():
    """Tạo kết nối đến cơ sở dữ liệu MySQL."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="qlthucung"
    )

def is_owner_exist(owner_id):
    """Kiểm tra xem ID chủ sở hữu có tồn tại trong bảng chu_so_huu không."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM chu_so_huu WHERE id = %s", (owner_id,))
    owner = cursor.fetchone()
    cursor.close()
    connection.close()
    return owner is not None

def add_pet(pet):
    """Thêm một vật nuôi mới vào bảng thu_cung."""
    if not is_owner_exist(pet["ID chủ vật nuôi"]):
        print("Lỗi: ID chủ vật nuôi không tồn tại!")
        return
    
    connection = create_connection()
    cursor = connection.cursor()
    sql = """
    INSERT INTO thu_cung (id, ten, loai, tuoi, gioi_tinh, id_chu_so_huu)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (
        pet["ID vật nuôi"], pet["Tên vật nuôi"], pet["Loài"],
        pet["Tuổi"], pet["Giới tính"], pet["ID chủ vật nuôi"]
    ))
    connection.commit()
    cursor.close()
    connection.close()

def delete_pet(pet_id):
    """Xóa một vật nuôi khỏi bảng thu_cung bằng ID."""
    connection = create_connection()
    cursor = connection.cursor()
    sql = "DELETE FROM thu_cung WHERE id = %s"
    cursor.execute(sql, (pet_id,))
    connection.commit()
    cursor.close()
    connection.close()

def update_pet(updated_pet):
    """Cập nhật thông tin của một vật nuôi."""
    if not is_owner_exist(updated_pet["ID chủ vật nuôi"]):
        print("Lỗi: ID chủ vật nuôi không tồn tại!")
        return
    
    connection = create_connection()
    cursor = connection.cursor()
    sql = """
    UPDATE thu_cung
    SET ten = %s, loai = %s, tuoi = %s, gioi_tinh = %s, id_chu_so_huu = %s
    WHERE id = %s
    """
    cursor.execute(sql, (
        updated_pet["Tên vật nuôi"], updated_pet["Loài"], updated_pet["Tuổi"],
        updated_pet["Giới tính"], updated_pet["ID chủ vật nuôi"], updated_pet["ID vật nuôi"]
    ))
    connection.commit()
    cursor.close()
    connection.close()

def search_pets(keyword, field):
    """Tìm kiếm vật nuôi theo một trường cụ thể."""
    connection = create_connection()
    cursor = connection.cursor()
    sql = f"SELECT * FROM thu_cung WHERE {field} LIKE %s"
    cursor.execute(sql, ('%' + keyword + '%',))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def get_all_pets():
    """Lấy danh sách tất cả vật nuôi trong hệ thống."""
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM thu_cung")
    pets = cursor.fetchall()
    cursor.close()
    connection.close()
    return pets
