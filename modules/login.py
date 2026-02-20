import customtkinter as ctk
import sqlite3
from cashier import open_cashier


def open_login():

    ctk.set_appearance_mode("dark")

    root = ctk.CTk()
    root.title("تسجيل الدخول")
    root.state("zoomed")

    # ===== العنوان =====
    title = ctk.CTkLabel(root,
                         text="تسجيل الدخول",
                         font=("Cairo", 26),
                         text_color="#C9A227")
    title.pack(pady=40)

    # ===== اسم المستخدم =====
    username = ctk.CTkEntry(root,
                            placeholder_text="اسم المستخدم",
                            font=("Cairo", 16),
                            width=300)
    username.pack(pady=10)

    # ===== كلمة المرور (مشفرة) =====
    password = ctk.CTkEntry(root,
                            placeholder_text="كلمة المرور",
                            show="*",   # تشفير الباسورد
                            font=("Cairo", 16),
                            width=300)
    password.pack(pady=10)

    # ===== رسالة الحالة =====
    result = ctk.CTkLabel(root,
                          text="",
                          font=("Cairo", 14))
    result.pack()

    # ===== وظيفة تسجيل الدخول =====
    def login():

        user = username.get().strip()
        pas = password.get().strip()

        # منع الإدخال الفارغ
        if not user or not pas:
            result.configure(text="يرجى إدخال اسم المستخدم وكلمة المرور",
                             text_color="orange")
            return

        try:
            con = sqlite3.connect("data.db")
            cur = con.cursor()

            cur.execute(
                "SELECT role FROM accounts WHERE username=? AND password=?",
                (user, pas)
            )

            data = cur.fetchone()

            con.close()

            if data:
                role = data[0]

                result.configure(text="تم تسجيل الدخول بنجاح",
                                 text_color="green")

                root.update()

                root.destroy()

                open_cashier(user, role)

            else:
                result.configure(text="بيانات الدخول غير صحيحة",
                                 text_color="red")

        except Exception as e:
            result.configure(text="حدث خطأ في الاتصال بقاعدة البيانات",
                             text_color="red")
            print("Login Error:", e)

    # ===== زر الدخول =====
    btn = ctk.CTkButton(root,
                        text="دخول",
                        fg_color="#C9A227",
                        text_color="black",
                        font=("Cairo", 16),
                        command=login)

    btn.pack(pady=20)

    # ===== دعم زر Enter =====
    root.bind("<Return>", lambda event: login())

    root.mainloop()
