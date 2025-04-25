# import views/login_view.py
import sys
import os
import customtkinter as ctk
from PIL import Image
from controllers.login_controller import LoginController

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def show_login_content(root, open_home_callback):
    import views.main_view as main_view
    login_controller = LoginController()

    # Nhập register_view tại đây để tránh circular import
    import views.register_view as register_view

    # Tạo frame chứa giao diện đăng nhập
    login_frame = ctk.CTkFrame(root, fg_color="#fff")
    login_frame.pack(fill="both", expand=True)

    def open_home():
        # Xóa giao diện đăng nhập
        login_frame.destroy()
        # Gọi callback để hiển thị giao diện menu
        open_home_callback(root)

    def switch_to_register():
        # Xóa giao diện đăng nhập
        login_frame.destroy()
        # Hiển thị giao diện đăng ký, truyền root, callback để quay lại login và open_home_callback
        register_view.show_register_content(root, show_login_content, open_home_callback)

    # Load hình ảnh logo với CTkImage
    try:
        img = Image.open("images/login.png")
        img = img.resize((400, 400), Image.Resampling.LANCZOS)
        photo = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 400))
    except Exception as e:
        print(f"Lỗi tải ảnh: {e}")
        photo = None

    if photo:
        label = ctk.CTkLabel(login_frame, image=photo, text="")
        label.image = photo  # Giữ tham chiếu
        label.place(x=50, y=50)

    # Khung đăng nhập
    frame = ctk.CTkFrame(login_frame, width=350, height=350, fg_color="white")
    frame.place(x=480, y=70)

    heading = ctk.CTkLabel(frame, text="Sign in", text_color="#57a1f8", fg_color="white",
                           font=("Microsoft YaHei UI Light", 23, "bold"))
    heading.place(x=100, y=5)

    # Ô nhập Username
    def on_enter_user(event):
        if user.get() == "Username":
            user.delete(0, "end")

    def on_leave_user(event):
        if not user.get():
            user.insert(0, "Username")

    user = ctk.CTkEntry(frame, width=250, text_color="black", fg_color="white",
                        border_width=0, font=("Microsoft YaHei UI Light", 11),
                        placeholder_text="Username", placeholder_text_color="gray")
    user.place(x=30, y=80)
    user.insert(0, "Username")
    user.bind("<FocusIn>", on_enter_user)
    user.bind("<FocusOut>", on_leave_user)

    underline_user = ctk.CTkFrame(frame, width=295, height=2, fg_color="black")
    underline_user.place(x=25, y=107)

    # Ô nhập Password
    def on_enter_pass(event):
        if password.get() == "Password":
            password.delete(0, "end")
            password.configure(show="*")

    def on_leave_pass(event):
        if not password.get():
            password.insert(0, "Password")
            password.configure(show="")

    password = ctk.CTkEntry(frame, width=250, text_color="black", fg_color="white",
                            border_width=0, font=("Microsoft YaHei UI Light", 11),
                            placeholder_text="Password", placeholder_text_color="gray")
    password.place(x=30, y=150)
    password.insert(0, "Password")
    password.bind("<FocusIn>", on_enter_pass)
    password.bind("<FocusOut>", on_leave_pass)

    underline_pass = ctk.CTkFrame(frame, width=295, height=2, fg_color="black")
    underline_pass.place(x=25, y=177)

    # Xử lý đăng nhập
    def handle_login():
        username = user.get().strip()
        pwd = password.get().strip()
        if username == "Username":
            username = ""
        if pwd == "Password":
            pwd = ""
        success, message = login_controller.login(username, pwd, open_home)
        if success:
            open_home()  # Chuyển sang giao diện chính khi thành công và 
        else:
            error_label.configure(text=message)
            

    # Nút đăng nhập
    login_button = ctk.CTkButton(frame, width=295, height=40, text="Sign in",
                                 fg_color="#57a1f8", text_color="white", font=("Microsoft YaHei UI Light", 11),
                                 command=handle_login)
    login_button.place(x=35, y=204)

    # Hiển thị lỗi đăng nhập
    error_label = ctk.CTkLabel(frame, text="", text_color="red", fg_color="white",
                               font=("Microsoft YaHei UI Light", 11))
    error_label.place(x=30, y=240)

    # Nhãn và nút đăng ký
    ctk.CTkLabel(frame, text="Don't have an account?", fg_color="white",
                 text_color="#57a1f8", font=("Microsoft YaHei UI Light", 9)).place(x=75, y=270)

    sign_up = ctk.CTkButton(frame, width=60, text="Sign up",
                            fg_color="white", text_color="#57a1f8", font=("Microsoft YaHei UI Light", 9),
                            hover=False, command=switch_to_register)
    sign_up.place(x=215, y=270)

    return login_frame