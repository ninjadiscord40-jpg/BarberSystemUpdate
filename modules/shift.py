import customtkinter as ctk
import sqlite3
import os
from datetime import datetime
from tkinter import ttk

from approve import check_admin_password
from reports import report_shift_close
from password_dialog import ask_password


def show_message(title, text):

    msg = ctk.CTkToplevel()
    msg.title(title)
    msg.geometry("350x150")
    msg.grab_set()

    ctk.CTkLabel(
        msg,
        text=text,
        font=("Cairo", 14)
    ).pack(pady=20)

    ctk.CTkButton(
        msg,
        text="حسناً",
        command=msg.destroy
    ).pack()


def info_box(parent, title, value, color="#2ECC71"):

    box = ctk.CTkFrame(
        parent,
        width=250,
        height=120,
        fg_color="#1E1E1E"
    )

    box.pack_propagate(False)

    ctk.CTkLabel(
        box,
        text=title,
        font=("Cairo", 14),
        text_color="#C9A227"
    ).pack(pady=5)

    ctk.CTkLabel(
        box,
        text=str(round(float(value), 2)),
        font=("Cairo", 22, "bold"),
        text_color=color
    ).pack(pady=5)

    return box


def open_shift_close(user):

    win = ctk.CTkToplevel()
    win.title("إغلاق الشفت")
    win.state("zoomed")
    win.grab_set()

    title = ctk.CTkLabel(
        win,
        text="تفاصيل الشفت الحالي",
        font=("Cairo", 22),
        text_color="#C9A227"
    )

    title.pack(pady=20)

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    # ===== جلب العهدة المستلمة من آخر شفت (ثابتة) =====

    cur.execute(
        "SELECT received_balance FROM shift ORDER BY id DESC LIMIT 1"
    )

    last_shift = cur.fetchone()

    if last_shift:
        start_balance = float(last_shift[0])
    else:
        start_balance = 0

    # ===== الحسابات الحالية =====

    cur.execute("SELECT SUM(total) FROM orders")
    sales = cur.fetchone()[0] or 0

    cur.execute(
        "SELECT SUM(amount) FROM cash_actions WHERE type='add'"
    )
    added = cur.fetchone()[0] or 0

    cur.execute(
        "SELECT SUM(amount) FROM cash_actions WHERE type='remove'"
    )
    removed = cur.fetchone()[0] or 0

    cur.execute("SELECT SUM(discount) FROM orders")
    discounts = cur.fetchone()[0] or 0

    # ===== إجمالي الدرج (المتحرك) =====

    total_drawer = start_balance + sales + added - removed

    con.close()

    # ===== مربعات الإحصائيات =====

    stats = ctk.CTkFrame(
        win,
        fg_color="#252525"
    )

    stats.pack(pady=10)

    # إجمالي الدرج (يتغير)
    info_box(
        stats,
        "إجمالي الدرج",
        total_drawer,
        "#2ECC71"
    ).grid(row=0, column=0, padx=20, pady=20)

    # العهدة المستلمة (ثابتة)
    info_box(
        stats,
        "العهدة المستلمة",
        start_balance,
        "#F1C40F"
    ).grid(row=0, column=1, padx=20, pady=20)

    info_box(
        stats,
        "إجمالي المبيعات",
        sales
    ).grid(row=0, column=2, padx=20, pady=20)

    info_box(
        stats,
        "إجمالي الإضافات",
        added,
        "#3498DB"
    ).grid(row=0, column=3, padx=20, pady=20)

    info_box(
        stats,
        "إجمالي الإخراج",
        removed,
        "#E74C3C"
    ).grid(row=0, column=4, padx=20, pady=20)

    info_box(
        stats,
        "إجمالي الخصومات",
        discounts,
        "#F39C12"
    ).grid(row=0, column=5, padx=20, pady=20)

    # ===== جدول السجل =====

    log_frame = ctk.CTkFrame(
        win,
        fg_color="#252525"
    )

    log_frame.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    columns = (
        "type",
        "number",
        "amount",
        "discount",
        "note",
        "user",
        "date"
    )

    tree = ttk.Treeview(
        log_frame,
        columns=columns,
        show="headings"
    )

    tree.pack(fill="both", expand=True)

    tree.heading("type", text="النوع")
    tree.heading("number", text="رقم العملية")
    tree.heading("amount", text="المبلغ")
    tree.heading("discount", text="الخصم")
    tree.heading("note", text="ملاحظة")
    tree.heading("user", text="الموظف")
    tree.heading("date", text="التاريخ")

    # ===== تحميل البيانات =====

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    # تحميل الأوردرات
    cur.execute(
        "SELECT order_number,total,discount,barber,date FROM orders"
    )

    for o in cur.fetchall():

        tree.insert(
            "",
            "end",
            values=(
                "أوردر",
                o[0],
                o[1],
                o[2],
                "",
                o[3],
                o[4]
            )
        )

    # تحميل الإضافات والإخراج
    cur.execute(
        "SELECT type,amount,note,date FROM cash_actions"
    )

    for c in cur.fetchall():

        t = "إضافة مال" if c[0] == "add" else "إخراج مال"

        tree.insert(
            "",
            "end",
            values=(
                t,
                "",
                c[1],
                "",
                c[2],
                user,
                c[3]
            )
        )

    con.close()

    # ===== إغلاق الشفت =====

    def close_shift():

        admin_pass = ask_password(
            "تأكيد إغلاق الشفت",
            "أدخل باسورد الأدمن"
        )

        if not admin_pass:
            return

        admin = check_admin_password(admin_pass)

        if not admin:

            show_message(
                "خطأ",
                "باسورد الأدمن غير صحيح"
            )

            return

        # إرسال التقرير
        report_shift_close(
            sales,
            added,
            removed,
            total_drawer,
            user
        )

        con = sqlite3.connect("data.db")
        cur = con.cursor()

        # حفظ الشفت الجديد
        cur.execute("""
            INSERT INTO shift(
                start_balance,
                added_money,
                removed_money,
                total_sales,
                received_balance,
                date
            )
            VALUES(?,?,?,?,?,?)
        """, (
            start_balance,
            added,
            removed,
            sales,
            total_drawer,
            datetime.now()
        ))

        # تصفير العمليات فقط
        cur.execute("DELETE FROM orders")
        cur.execute("DELETE FROM order_items")
        cur.execute("DELETE FROM cash_actions")

        con.commit()
        con.close()

        show_message(
            "تم",
            "تم إغلاق الشفت بنجاح – سيتم إغلاق البرنامج"
        )

        os._exit(0)

    ctk.CTkButton(
        win,
        text="إغلاق الشفت نهائيًا",
        fg_color="#E74C3C",
        font=("Cairo", 18),
        command=close_shift
    ).pack(pady=20)
