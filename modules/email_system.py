import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ===== بيانات الإيميل =====
SENDER_EMAIL = "youssefmoneer19@gmail.com"
SENDER_PASSWORD = "hlir lkpc adtu jzck"
RECEIVER_EMAIL = "shadyromany41@gmail.com"


def send_email(subject, message):

    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain", "utf-8"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        return True

    except Exception as e:
        print("Email Error:", e)
        return False
