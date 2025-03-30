# views/register_view.py
import customtkinter as ctk
from PIL import Image
from controllers.register_controller import RegisterController

def show_register_content(root, open_login_callback, open_home_callback):
    # Nhập show_login_content tại đây để tránh circular import
    from views.login_view import show_login_content

    register_controller = RegisterController()

    # Tạo frame chứa giao diện đăng ký
    register_frame = ctk.CTkFrame(root, fg_color="#fff")
    register_frame.pack(fill="both", expand=True)

    def open_login():
        # Xóa giao diện đăng ký
        register_frame.destroy()
        # Gọi callback để hiển thị giao diện đăng nhập
        open_login_callback(root, open_home_callback)

    def switch_to_login():
        # Xóa giao diện đăng ký
        register_frame.destroy()
        # Hiển thị lại giao diện đăng nhập
        open_login_callback(root, open_home_callback)

    # Load hình ảnh logo với CTkImage (dùng cùng file ảnh login.png)
    try:
        img = Image.open("image/login.png")
        img = img.resize((400, 400), Image.Resampling.LANCZOS)
        photo = ctk.CTkImage(light_image=img, dark_image=img, size=(400, 400))
    except Exception as e:
        print(f"Lỗi tải ảnh: {e}")
        photo = None

    if photo:
        label = ctk.CTkLabel(register_frame, image=photo, text="")
        label.image = photo  # Giữ tham chiếu
        label.place(x=50, y=50)

    # Khung đăng ký
    frame = ctk.CTkFrame(register_frame, width=350, height=450, fg_color="white")
    frame.place(x=480, y=70)

    heading = ctk.CTkLabel(frame, text="Sign up", text_color="#57a1f8", fg_color="white",
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
    user.place(x=30, y=60)  # Giảm y từ 80 xuống 60
    user.insert(0, "Username")
    user.bind("<FocusIn>", on_enter_user)
    user.bind("<FocusOut>", on_leave_user)

    underline_user = ctk.CTkFrame(frame, width=295, height=2, fg_color="black")
    underline_user.place(x=25, y=87)  # Giảm y từ 107 xuống 87

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
    password.place(x=30, y=110)  # Giảm y từ 150 xuống 110
    password.insert(0, "Password")
    password.bind("<FocusIn>", on_enter_pass)
    password.bind("<FocusOut>", on_leave_pass)

    underline_pass = ctk.CTkFrame(frame, width=295, height=2, fg_color="black")
    underline_pass.place(x=25, y=137)  # Giảm y từ 177 xuống 137

    # Ô nhập Confirm Password
    def on_enter_confirm(event):
        if confirm_password.get() == "Confirm Password":
            confirm_password.delete(0, "end")
            confirm_password.configure(show="*")

    def on_leave_confirm(event):
        if not confirm_password.get():
            confirm_password.insert(0, "Confirm Password")
            confirm_password.configure(show="")

    confirm_password = ctk.CTkEntry(frame, width=250, text_color="black", fg_color="white",
                                    border_width=0, font=("Microsoft YaHei UI Light", 11),
                                    placeholder_text="Confirm Password", placeholder_text_color="gray")
    confirm_password.place(x=30, y=160)  # Giảm y từ 220 xuống 160
    confirm_password.insert(0, "Confirm Password")
    confirm_password.bind("<FocusIn>", on_enter_confirm)
    confirm_password.bind("<FocusOut>", on_leave_confirm)

    underline_confirm = ctk.CTkFrame(frame, width=295, height=2, fg_color="black")
    underline_confirm.place(x=25, y=187)  # Giảm y từ 247 xuống 187

    # Ô nhập Email
    def on_enter_email(event):
        if email.get() == "Email":
            email.delete(0, "end")

    def on_leave_email(event):
        if not email.get():
            email.insert(0, "Email")

    email = ctk.CTkEntry(frame, width=250, text_color="black", fg_color="white",
                         border_width=0, font=("Microsoft YaHei UI Light", 11),
                         placeholder_text="Email", placeholder_text_color="gray")
    email.place(x=30, y=210)  # Giảm y từ 290 xuống 210
    email.insert(0, "Email")
    email.bind("<FocusIn>", on_enter_email)
    email.bind("<FocusOut>", on_leave_email)

    underline_email = ctk.CTkFrame(frame, width=295, height=2, fg_color="black")
    underline_email.place(x=25, y=237)  # Giảm y từ 317 xuống 237

    # Xử lý đăng ký
    def handle_register():
        username = user.get().strip()
        pwd = password.get().strip()
        confirm_pwd = confirm_password.get().strip()
        mail = email.get().strip()
        if username == "Username":
            username = ""
        if pwd == "Password":
            pwd = ""
        if confirm_pwd == "Confirm Password":
            confirm_pwd = ""
        if mail == "Email":
            mail = ""
        success, message = register_controller.register(username, pwd, confirm_pwd, mail, open_login)
        if not success:
            error_label.configure(text=message)

    # Nút đăng ký
    register_button = ctk.CTkButton(frame, width=295, height=40, text="Sign up",
                                    fg_color="#57a1f8", text_color="white", font=("Microsoft YaHei UI Light", 11),
                                    command=handle_register)
    register_button.place(x=35, y=264)  # Giảm y từ 344 xuống 264

    # Hiển thị lỗi đăng ký
    error_label = ctk.CTkLabel(frame, text="", text_color="red", fg_color="white",
                               font=("Microsoft YaHei UI Light", 11))
    error_label.place(x=30, y=310)  # Giảm y từ 390 xuống 310

    # Nhãn và nút quay lại đăng nhập
    ctk.CTkLabel(frame, text="Already have an account?", fg_color="white",
                 text_color="#57a1f8", font=("Microsoft YaHei UI Light", 9)).place(x=75, y=340)  # Giảm y từ 420 xuống 340

    sign_in = ctk.CTkButton(frame, width=60, text="Sign in",
                            fg_color="white", text_color="#57a1f8", font=("Microsoft YaHei UI Light", 9),
                            hover=False, command=switch_to_login)
    sign_in.place(x=215, y=340)  # Giảm y từ 420 xuống 340

    return register_frame