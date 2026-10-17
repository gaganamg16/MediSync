from django.contrib import admin
from .models import Profile, DoctorPatient


@admin.register(DoctorPatient)
class DoctorPatientAdmin(admin.ModelAdmin):
    list_display = ("doctor", "patient", "created_at")
    list_filter = ("created_at",)
    search_fields = (
        "doctor__username",
        "patient__username",
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone_number", "created_at")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email")