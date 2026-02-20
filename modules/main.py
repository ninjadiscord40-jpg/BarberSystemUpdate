import customtkinter as ctk
import time

from database import create_tables
from init_system import setup
from login import open_login

ctk.set_appearance_mode("dark")

# إنشاء الجداول أول تشغيل
create_tables()
setup()

root = ctk.CTk()
root.geometry("500x300")
root.title("Barber System")

# ===== العنوان =====
label = ctk.CTkLabel(
    root,
    text="اهلا بيك تاتيس & شادي",
    font=("Cairo", 22),
    text_color="#C9A227"
)
label.pack(pady=80)

# ===== شريط التحميل =====
progress = ctk.CTkProgressBar(root, width=300)
progress.pack(pady=20)
progress.set(0)

# ===== النص السفلي (حقوق النسخة) =====
footer = ctk.CTkLabel(
    root,
    text="هذا تحديث v3.5.2 مصمم عن طريق نينجا — جميع الحقوق محفوظة © Ninja",
    font=("Cairo", 12),
    text_color="#888888"
)
footer.pack(side="bottom", pady=10)


# ===== التحميل =====
def load():
    for i in range(101):
        progress.set(i / 100)
        root.update()
        time.sleep(0.01)

    root.destroy()
    open_login()


root.after(500, load)

root.mainloop()
