import customtkinter as ctk


def ask_password(title="إدخال كلمة المرور", text="أدخل كلمة المرور"):

    result = {"value": None}

    win = ctk.CTkToplevel()
    win.title(title)
    win.geometry("320x160")
    win.grab_set()

    ctk.CTkLabel(win,
                 text=text,
                 font=("Cairo", 14)).pack(pady=10)

    entry = ctk.CTkEntry(win,
                         show="*",
                         font=("Cairo", 14),
                         width=200)
    entry.pack(pady=5)
    entry.focus()

    def submit():
        result["value"] = entry.get()
        win.destroy()

    ctk.CTkButton(win,
                  text="موافق",
                  command=submit,
                  fg_color="#C9A227",
                  text_color="black").pack(pady=10)

    win.wait_window()

    return result["value"]
