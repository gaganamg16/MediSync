from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

class Medicine(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)

    start_date = models.DateField()
    end_date = models.DateField()

    reminder_time = models.TimeField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
class MedicineReminderLog(models.Model):
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.CASCADE,
        related_name="reminder_logs",
    )
    reminder_date = models.DateField()
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["medicine", "reminder_date"],
                name="unique_medicine_reminder_per_day",
            )
        ]

    def __str__(self):
        return f"{self.medicine.name} - {self.reminder_date}"  

class Prescription(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_prescriptions",
    )
    patient = models.ForeignKey(
             User,
             on_delete=models.CASCADE,
             related_name="received_prescriptions",
             null=True,
             blank=True,
    )
    
    medicine_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.medicine_name} - {self.patient.username}"
