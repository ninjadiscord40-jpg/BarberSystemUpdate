import sqlite3
from email_system import send_email
from datetime import datetime


def report_cash_action(action_type, amount, note, user):

    title = "إضافة مال" if action_type == "add" else "إخراج مال"

    message = f"""
    نوع العملية : {title}
    المبلغ      : {amount}
    الملاحظة    : {note}
    المستخدم    : {user}
    التاريخ     : {datetime.now()}
    """

    send_email(f"تقرير: {title}", message)


def report_shift_close(sales, added, removed, final_total, user):

    message = f"""
    ===== تقرير إغلاق شفت =====

    المستخدم القائم بالإغلاق : {user}

    إجمالي المبيعات : {sales}
    إجمالي الإضافات : {added}
    إجمالي الإخراج  : {removed}

    الرصيد النهائي : {final_total}

    التاريخ : {datetime.now()}
    """

    send_email("تقرير إغلاق شفت", message)
