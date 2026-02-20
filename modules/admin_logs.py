import customtkinter as ctk
import sqlite3
from datetime import datetime
from tkinter import ttk

from reports import report_cash_action


def show_message(title, text):
    msg = ctk.CTkToplevel()
    msg.title(title)
    msg.geometry("350x160")
    msg.grab_set()

    ctk.CTkLabel(msg, text=text, font=("Cairo", 14)).pack(pady=20)
    ctk.CTkButton(msg, text="حسناً", command=msg.destroy).pack()


def show_cash_details(values):

    win = ctk.CTkToplevel()
    win.title("تفاصيل العملية")
    win.geometry("400x300")
    win.grab_set()

    labels = [
        ("النوع", values[1]),
        ("المبلغ", values[2]),
        ("المستخدم", values[3]),
        ("الموافقة", values[4]),
        ("الملاحظة", values[5]),
        ("التاريخ", values[6]),
        ("الوقت", values[7]),
    ]

    for title, val in labels:

        frame = ctk.CTkFrame(win)
        frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(frame, text=title + ":", width=120).pack(side="left")

        ctk.CTkLabel(
            frame,
            text=str(val),
            text_color="#C9A227"
        ).pack(side="left")


def show_shift_details(values):

    win = ctk.CTkToplevel()
    win.title("تفاصيل الشفت")
    win.geometry("400x350")
    win.grab_set()

    labels = [
        ("رقم الشفت", values[0]),
        ("الرصيد بالبداية", values[1]),
        ("الإضافات", values[2]),
        ("الإخراج", values[3]),
        ("إجمالي المبيعات", values[4]),
        ("الرصيد النهائي", values[5]),
        ("التاريخ", values[6]),
    ]

    for title, val in labels:

        frame = ctk.CTkFrame(win)
        frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(frame, text=title + ":", width=150).pack(side="left")

        ctk.CTkLabel(
            frame,
            text=str(val),
            text_color="#C9A227"
        ).pack(side="left")


def open_admin_panel(user, refresh_callback=None):

    win = ctk.CTkToplevel()
    win.title("لوحة الإدارة")
    win.state("zoomed")
    win.grab_set()

    tab = ctk.CTkTabview(win)
    tab.pack(fill="both", expand=True)

    tab.add("إضافة صنف")
    tab.add("إضافة حساب")
    tab.add("إضافة موظف")
    tab.add("إضافة مال")
    tab.add("إخراج مال")
    tab.add("التقارير")
    tab.add("سجل الإضافة والإخراج")
    tab.add("سجل إغلاق الشفت")
    
    # ===== Customer System =====
    tab.add("سجل العملاء")

    # ===== إضافة صنف =====
    frame = tab.tab("إضافة صنف")

    name = ctk.CTkEntry(frame, placeholder_text="اسم الصنف")
    name.pack(pady=10)

    price = ctk.CTkEntry(frame, placeholder_text="السعر")
    price.pack(pady=10)

    def add_service():

        con = sqlite3.connect("data.db")
        cur = con.cursor()

        cur.execute(
            "INSERT INTO services(name, price) VALUES(?,?)",
            (name.get(), price.get())
        )

        con.commit()
        con.close()

        show_message("تم", "تم إضافة الصنف بنجاح")

        if refresh_callback:
            refresh_callback()

    ctk.CTkButton(frame, text="إضافة", command=add_service).pack()

    # ===== إضافة حساب =====
    frame2 = tab.tab("إضافة حساب")

    u = ctk.CTkEntry(frame2, placeholder_text="اسم المستخدم")
    u.pack(pady=10)

    p = ctk.CTkEntry(frame2, placeholder_text="كلمة المرور")
    p.pack(pady=10)

    role = ctk.CTkComboBox(frame2, values=["admin", "cashier"])
    role.pack(pady=10)

    def add_account():

        con = sqlite3.connect("data.db")
        cur = con.cursor()

        cur.execute(
            "INSERT INTO accounts(username,password,role) VALUES(?,?,?)",
            (u.get(), p.get(), role.get())
        )

        con.commit()
        con.close()

        show_message("تم", "تم إضافة الحساب بنجاح")

    ctk.CTkButton(frame2, text="حفظ", command=add_account).pack()

    # ===== إضافة موظف =====
    frame3 = tab.tab("إضافة موظف")

    emp = ctk.CTkEntry(frame3, placeholder_text="اسم الموظف")
    emp.pack(pady=10)

    def add_barber():

        con = sqlite3.connect("data.db")
        cur = con.cursor()

        cur.execute("INSERT INTO barbers(name) VALUES(?)", (emp.get(),))

        con.commit()
        con.close()

        show_message("تم", "تم إضافة الموظف بنجاح")

    ctk.CTkButton(frame3, text="إضافة", command=add_barber).pack()

    # ===== إضافة مال =====
    frame4 = tab.tab("إضافة مال")

    amount = ctk.CTkEntry(frame4, placeholder_text="المبلغ")
    amount.pack(pady=10)

    note = ctk.CTkEntry(frame4, placeholder_text="ملاحظة")
    note.pack(pady=10)

    def add_money():

        now = datetime.now()

        con = sqlite3.connect("data.db")
        cur = con.cursor()

        cur.execute(
            "INSERT INTO cash_actions(type,amount,note,date) VALUES(?,?,?,?)",
            ("add", amount.get(), note.get(), now)
        )

        cur.execute("""
            INSERT INTO cash_log
            (type,amount,note,created_by,approved_by,date,time,datetime)
            VALUES(?,?,?,?,?,?,?,?)
        """, (
            "إضافة",
            amount.get(),
            note.get(),
            user,
            user,
            now.date(),
            now.strftime("%H:%M"),
            now
        ))

        con.commit()
        con.close()

        report_cash_action("add", amount.get(), note.get(), user)

        show_message("تم", "تم إضافة المال بنجاح")

    ctk.CTkButton(frame4, text="تنفيذ", command=add_money).pack()

    # ===== إخراج مال =====
    frame5 = tab.tab("إخراج مال")

    amount2 = ctk.CTkEntry(frame5, placeholder_text="المبلغ")
    amount2.pack(pady=10)

    note2 = ctk.CTkEntry(frame5, placeholder_text="ملاحظة")
    note2.pack(pady=10)

    def remove_money():

        now = datetime.now()

        con = sqlite3.connect("data.db")
        cur = con.cursor()

        cur.execute(
            "INSERT INTO cash_actions(type,amount,note,date) VALUES(?,?,?,?)",
            ("remove", amount2.get(), note2.get(), now)
        )

        cur.execute("""
            INSERT INTO cash_log
            (type,amount,note,created_by,approved_by,date,time,datetime)
            VALUES(?,?,?,?,?,?,?,?)
        """, (
            "إخراج",
            amount2.get(),
            note2.get(),
            user,
            user,
            now.date(),
            now.strftime("%H:%M"),
            now
        ))

        con.commit()
        con.close()

        report_cash_action("remove", amount2.get(), note2.get(), user)

        show_message("تم", "تم إخراج المال بنجاح")

    ctk.CTkButton(frame5, text="تنفيذ", command=remove_money).pack()

    # ===== Customer System =====
    frame_customers = tab.tab("سجل العملاء")

    customer_columns = ("id", "name", "phone", "created_at")

    customer_tree = ttk.Treeview(
        frame_customers,
        columns=customer_columns,
        show="headings"
    )

    customer_tree.pack(fill="both", expand=True)

    titles = ["ID", "الاسم", "الموبايل", "تاريخ التسجيل"]

    for col, title in zip(customer_columns, titles):
        customer_tree.heading(col, text=title)

    def load_customers():

        customer_tree.delete(*customer_tree.get_children())

        con = sqlite3.connect("data.db")
        cur = con.cursor()

        cur.execute("""
            SELECT id, name, phone, created_at
            FROM customers
            ORDER BY id DESC
        """)

        for row in cur.fetchall():
            customer_tree.insert("", "end", values=row)

        con.close()

    ctk.CTkButton(
        frame_customers,
        text="تحديث",
        command=load_customers
    ).pack(pady=5)

    load_customers()

    # باقي الملف كما هو بدون أي تعديل...