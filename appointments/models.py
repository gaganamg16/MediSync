from django.db import models
from django.contrib.auth.models import User


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    doctor_name = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=150)

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor_name} - {self.appointment_date}"
    
class AppointmentReminderLog(models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name="reminder_logs",
    )
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["appointment"],
                name="unique_appointment_reminder",
            )
        ]

    def __str__(self):
        return f"Reminder for {self.appointment}"