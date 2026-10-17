from django.contrib import admin
from .models import Medicine, MedicineReminderLog, Prescription

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
  list_display = ("name", "user", "dosage", "start_date", "end_date")

@admin.register(MedicineReminderLog)
class MedicineReminderLogAdmin(admin.ModelAdmin):
  list_display = ("medicine", "reminder_date", "sent_at")

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
 list_display = (
"medicine_name",
"doctor",
"patient",
"dosage",
"start_date",
"end_date",
)
list_filter = ("start_date", "end_date")
search_fields = (
"medicine_name",
"doctor__username",
"patient__username",
)
