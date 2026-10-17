from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):

    ROLE_CHOICES = [
        ("PATIENT", "Patient"),
        ("DOCTOR", "Doctor"),
        ("ADMIN", "Admin"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="PATIENT"
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

class DoctorPatient(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_patient_links",
    )

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="patient_doctor_links",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "patient"],
                name="unique_doctor_patient_link",
            )
        ]

    def __str__(self):
        return f"{self.doctor.username} - {self.patient.username}"