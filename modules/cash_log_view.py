import customtkinter as ctk
import sqlite3
from tkinter import ttk
from datetime import datetime


def show_details(data):

    win = ctk.CTkToplevel()
    win.title("تفاصيل العملية")
    win.geometry("400x300")
    win.grab_set()

    labels = [
        ("النوع", data["type"]),
        ("المبلغ", data["amount"]),
        ("المستخدم", data["created_by"]),
        ("الموافقة", data["approved_by"]),
        ("الملاحظة", data["note"]),
        ("التاريخ", data["date"]),
        ("الوقت", data["time"]),
    ]

    for title, value in labels:

        frame = ctk.CTkFrame(win)
        frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            frame,
            text=f"{title}:",
            width=120,
            anchor="w",
            font=("Cairo", 14)
        ).pack(side="left", padx=5)

        ctk.CTkLabel(
            frame,
            text=str(value),
            anchor="w",
            font=("Cairo", 14),
            text_color="#C9A227"
        ).pack(side="left")


def open_cash_log():

    win = ctk.CTkToplevel()
    win.title("سجل الإضافة والإخراج")
    win.state("zoomed")
    win.grab_set()

    title = ctk.CTkLabel(
        win,
        text="سجل الإضافة والإخراج",
        font=("Cairo", 24),
        text_color="#C9A227"
    )
    title.pack(pady=10)

    # ===== فلترة =====

    filter_frame = ctk.CTkFrame(win)
    filter_frame.pack(fill="x", padx=10, pady=5)

    ctk.CTkLabel(filter_frame, text="من تاريخ:").pack(side="left", padx=5)

    from_date = ctk.CTkEntry(filter_frame, width=120)
    from_date.pack(side="left", padx=5)

    ctk.CTkLabel(filter_frame, text="إلى تاريخ:").pack(side="left", padx=5)

    to_date = ctk.CTkEntry(filter_frame, width=120)
    to_date.pack(side="left", padx=5)

    # ===== جدول =====

    table_frame = ctk.CTkFrame(win)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = (
        "id",
        "type",
        "amount",
        "created_by",
        "approved_by",
        "note",
        "date",
        "time"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    tree.heading("id", text="ID")
    tree.heading("type", text="النوع")
    tree.heading("amount", text="المبلغ")
    tree.heading("created_by", text="المستخدم")
    tree.heading("approved_by", text="الموافقة")
    tree.heading("note", text="الملاحظة")
    tree.heading("date", text="التاريخ")
    tree.heading("time", text="الوقت")

    tree.column("id", width=50)
    tree.column("type", width=100)
    tree.column("amount", width=100)
    tree.column("created_by", width=120)
    tree.column("approved_by", width=120)
    tree.column("note", width=200)
    tree.column("date", width=120)
    tree.column("time", width=120)

    tree.pack(fill="both", expand=True)

    # ===== تحميل البيانات =====

    def load_data():

        tree.delete(*tree.get_children())

        con = sqlite3.connect("data.db")
        cur = con.cursor()

        query = "SELECT * FROM cash_log WHERE 1=1"
        params = []

        if from_date.get():
            query += " AND date >= ?"
            params.append(from_date.get())

        if to_date.get():
            query += " AND date <= ?"
            params.append(to_date.get())

        query += " ORDER BY id DESC"

        cur.execute(query, params)

        for row in cur.fetchall():
            tree.insert("", "end", values=row)

        con.close()

    # ===== زر البحث =====

    ctk.CTkButton(
        filter_frame,
        text="بحث",
        command=load_data,
        fg_color="#3498DB"
    ).pack(side="left", padx=10)

    # ===== Double Click =====

    def on_double_click(event):

        selected = tree.selection()

        if not selected:
            return

        values = tree.item(selected[0])["values"]

        data = {
            "id": values[0],
            "type": values[1],
            "amount": values[2],
            "created_by": values[3],
            "approved_by": values[4],
            "note": values[5],
            "date": values[6],
            "time": values[7],
        }

        show_details(data)

    tree.bind("<Double-1>", on_double_click)

    # تحميل أولي
    load_data()
