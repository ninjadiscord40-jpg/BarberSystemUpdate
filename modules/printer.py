import os
from datetime import datetime


def print_receipt(order_number, items, total, barber, discount):

    try:
        receipt = ""
        receipt += "============================\n"
        receipt += "   Barber Shop System\n"
        receipt += "============================\n\n"

        receipt += f"Order No : {order_number}\n"
        receipt += f"Barber   : {barber}\n"
        receipt += f"Date     : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        receipt += "----------------------------\n"

        for i in items:
            receipt += f"{i[0]}  -  {i[1]}\n"

        receipt += "----------------------------\n"

        if discount:
            receipt += f"Discount : {discount}\n"

        receipt += f"Total    : {total}\n"
        receipt += "============================\n"
        receipt += "   Thank You!\n"
        receipt += "============================\n"

        # إنشاء ملف مؤقت للطباعة
        with open("receipt.txt", "w", encoding="utf-8") as f:
            f.write(receipt)

        # أمر الطباعة في الويندوز
        os.startfile("receipt.txt", "print")

        return True

    except Exception as e:
        print("Printing Error:", e)
        return False
