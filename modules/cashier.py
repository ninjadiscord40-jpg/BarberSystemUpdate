import customtkinter as ctk
import tkinter as tk
import sqlite3
import os
import threading
from playsound import playsound
from datetime import datetime

from order_system import get_next_order_number
from order_save import save_order
from barber_system import get_barbers
from approve import check_admin_password
from printer import print_receipt
from admin import open_admin_panel
from shift import open_shift_close
from password_dialog import ask_password


# ===== مسار الأصوات =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sounds")


def play_sound(file):
    try:
        path = os.path.join(SOUND_DIR, file)
        threading.Thread(
            target=playsound,
            args=(path,),
            daemon=True
        ).start()
    except Exception as e:
        print("Sound error:", e)


# ===== رسالة =====
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
        command=msg.destroy,
        font=("Cairo", 14)
    ).pack()


def open_cashier(user, role):

    ctk.set_appearance_mode("dark")

    app = ctk.CTk()
    app.state("zoomed")
    app.title("نظام كاشير صالون الحلاقة")

    cart = []

    top = ctk.CTkFrame(app, height=60, fg_color="#2D1B15")
    top.pack(fill="x")

    ctk.CTkLabel(
        top,
        text="نظام كاشير صالون الحلاقة",
        font=("Cairo", 20),
        text_color="white"
    ).pack(side="left", padx=20)

    ctk.CTkLabel(
        top,
        text=f"الحساب الحالي: {user}",
        font=("Cairo", 14),
        text_color="#C9A227"
    ).pack(side="right", padx=20)


    def switch_account():
        app.destroy()
        from login import open_login
        open_login()


    ctk.CTkButton(
        top,
        text="تبديل حساب سريع",
        fg_color="#1976D2",
        font=("Cairo", 14),
        command=switch_account
    ).pack(side="left", padx=5)
    # ===== زر إغلاق الشفت =====
    ctk.CTkButton(
        top,
        text="إغلاق شفت",
        fg_color="#E74C3C",
        font=("Cairo", 14),
        command=lambda: open_shift_close(user)
    ).pack(side="left", padx=5)


    def refresh_services():
        load_services()


    if role == "admin":

        ctk.CTkButton(
            top,
            text="إدارة",
            fg_color="#C9A227",
            text_color="black",
            font=("Cairo", 14),
            command=lambda: open_admin_panel(user, refresh_services)
        ).pack(side="left", padx=5)


    main = ctk.CTkFrame(app, fg_color="#1E1E1E")
    main.pack(fill="both", expand=True, padx=10, pady=10)

    left = ctk.CTkFrame(main, fg_color="#252525")
    left.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    right = ctk.CTkFrame(main, width=420, fg_color="#252525")
    right.pack(side="right", fill="y", padx=10, pady=10)


    ctk.CTkLabel(
        right,
        text="الكاشير",
        font=("Cairo", 18),
        text_color="#C9A227"
    ).pack(pady=10)


    barber_select = ctk.CTkComboBox(
        right,
        values=get_barbers(),
        font=("Cairo", 14)
    )
    barber_select.pack(pady=10)


    listbox = ctk.CTkTextbox(
        right,
        width=380,
        height=380,
        font=("Cairo", 14)
    )
    listbox.pack(pady=10)


    total_label = ctk.CTkLabel(
        right,
        text="الإجمالي: 0",
        font=("Cairo", 16),
        text_color="#2ECC71"
    )
    total_label.pack(pady=10)


    # ===== Customer Fields =====
    customer_name_entry = ctk.CTkEntry(
        right,
        placeholder_text="اسم العميل",
        font=("Cairo", 14)
    )
    customer_name_entry.pack(pady=5)

    customer_phone_entry = ctk.CTkEntry(
        right,
        placeholder_text="رقم الموبايل",
        font=("Cairo", 14)
    )
    customer_phone_entry.pack(pady=5)


    discount_entry = ctk.CTkEntry(
        right,
        placeholder_text="قيمة الخصم",
        font=("Cairo", 14)
    )
    discount_entry.pack(pady=5)


    def add_to_cart(name, price):

        cart.append((name, price))
        play_sound("add.wav")
        refresh_cart()


    def refresh_cart():

        listbox.delete("1.0", "end")

        total = 0

        for i in cart:

            listbox.insert("end", f"{i[0]} - {i[1]}\n")
            total += float(i[1])

        total_label.configure(text=f"الإجمالي: {total}")


    def clear_cart():
        cart.clear()
        refresh_cart()


    ctk.CTkButton(
        right,
        text="تفريغ السلة",
        fg_color="#E74C3C",
        command=clear_cart
    ).pack(pady=5)


    def finish_order():

        if not cart:
            show_message("تنبيه", "لا يوجد أوردر")
            return

        barber = barber_select.get()

        total = sum(float(i[1]) for i in cart)
        # ===== نظام الخصم (إصلاح مهم) =====
        discount = discount_entry.get()
        approved_by = ""

        if discount:

            admin_pass = ask_password(
                "تأكيد الخصم",
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

            approved_by = admin[0]

            total -= float(discount)

        # ===== حفظ العميل =====
        name = customer_name_entry.get().strip()
        phone = customer_phone_entry.get().strip()

        if name and phone:

            con = sqlite3.connect("data.db")
            cur = con.cursor()

            cur.execute("""
                INSERT OR IGNORE INTO customers(name, phone, created_at)
                VALUES(?,?,datetime('now'))
            """, (name, phone))

            con.commit()
            con.close()


        order_number = get_next_order_number()

        save_order(
            order_number,
            cart,
            total,
            barber,
            discount,
            approved_by,
            user
        )

        show_message("تم", f"تم حفظ الأوردر {order_number}")

        cart.clear()
        refresh_cart()


    ctk.CTkButton(
        right,
        text="تنفيذ الأوردر",
        fg_color="#C9A227",
        command=finish_order
    ).pack(pady=20)



    # ===== قائمة كليك يمين =====
    def show_service_menu(event, sid, name, price):
        menu = tk.Menu(app, tearoff=0)
        menu.add_command(
            label="تعديل",
            command=lambda: edit_service(sid, name, price)
        )
        menu.add_command(
            label="حذف",
            command=lambda: delete_service(sid)
        )
        menu.tk_popup(event.x_root, event.y_root)


    def edit_service(sid, old_name, old_price):

        win = ctk.CTkToplevel(app)
        win.title("تعديل الصنف")
        win.geometry("300x200")
        win.grab_set()

        name_entry = ctk.CTkEntry(win, font=("Cairo", 14))
        name_entry.insert(0, old_name)
        name_entry.pack(pady=10)

        price_entry = ctk.CTkEntry(win, font=("Cairo", 14))
        price_entry.insert(0, str(old_price))
        price_entry.pack(pady=10)

        def save_edit():
            new_name = name_entry.get().strip()
            new_price = price_entry.get().strip()

            if not new_name or not new_price:
                show_message("خطأ", "يرجى إدخال الاسم والسعر")
                return

            con = sqlite3.connect("data.db")
            cur = con.cursor()
            cur.execute(
                "UPDATE services SET name=?, price=? WHERE id=?",
                (new_name, new_price, sid)
            )
            con.commit()
            con.close()

            show_message("تم", "تم تعديل الصنف")
            win.destroy()
            load_services()

        ctk.CTkButton(
            win,
            text="حفظ",
            fg_color="#2ECC71",
            command=save_edit
        ).pack(pady=10)


    def delete_service(sid):

        win = ctk.CTkToplevel(app)
        win.title("تأكيد الحذف")
        win.geometry("300x150")
        win.grab_set()

        ctk.CTkLabel(
            win,
            text="هل أنت متأكد من الحذف؟",
            font=("Cairo", 14)
        ).pack(pady=20)

        def confirm():
            con = sqlite3.connect("data.db")
            cur = con.cursor()
            cur.execute("DELETE FROM services WHERE id=?", (sid,))
            con.commit()
            con.close()

            show_message("تم", "تم حذف الصنف")
            win.destroy()
            load_services()

        ctk.CTkButton(
            win,
            text="نعم",
            fg_color="#E74C3C",
            command=confirm
        ).pack(side="left", padx=20, pady=10)

        ctk.CTkButton(
            win,
            text="لا",
            command=win.destroy
        ).pack(side="right", padx=20, pady=10)


    # ===== تحميل الأصناف =====
    def load_services():

        for widget in left.winfo_children():
            widget.destroy()

        con = sqlite3.connect("data.db")
        cur = con.cursor()

        cur.execute("SELECT id,name,price FROM services")

        services = cur.fetchall()

        con.close()

        row = 0
        col = 0

        for sid, name, price in services:

            btn = ctk.CTkButton(
                left,
                text=f"{name}\n{price}",
                width=150,
                height=80,
                font=("Cairo", 18, "bold"),
                fg_color="#1f1f1f",
                hover_color="#C9A227",
                command=lambda n=name, p=price:
                add_to_cart(n, p)
            )

            btn.grid(row=row, column=col, padx=10, pady=10)

            btn.bind("<Button-3>", lambda e, sid=sid, n=name, p=price: show_service_menu(e, sid, n, p))

            col += 1
            if col == 4:
                col = 0
                row += 1


    load_services()

    app.mainloop()
