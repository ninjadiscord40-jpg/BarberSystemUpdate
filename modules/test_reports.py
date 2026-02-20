from reports import report_cash_action, report_shift_close

print("اختبار تقرير إضافة مال...")
report_cash_action("add", 100, "تجربة إضافة", "admin")

print("اختبار تقرير إخراج مال...")
report_cash_action("remove", 50, "تجربة إخراج", "admin")

print("اختبار تقرير إغلاق شفت...")
report_shift_close(500, 100, 50, 550, "admin")

print("تمت التجارب")
