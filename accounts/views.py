from .models import Profile
from medicines.models import Medicine, Prescription
from django.contrib import messages
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from appointments.models import Appointment
from records.models import MedicalRecord

def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(request, "accounts/home.html")
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)

        return redirect("dashboard")

    return render(request, "accounts/register.html")
@login_required
def dashboard(request):
    today = date.today()

    # Medicines
    medicines = Medicine.objects.filter(
        user=request.user
    )

    for medicine in medicines:
        if today < medicine.start_date:
            medicine.status = "Upcoming"
        elif today > medicine.end_date:
            medicine.status = "Completed"
        else:
            medicine.status = "Active"

    # Appointments
    appointments = Appointment.objects.filter(
        user=request.user
    ).order_by(
        "appointment_date",
        "appointment_time"
    )

    for appointment in appointments:
        if appointment.appointment_date < today:
            appointment.status = "Completed"
        elif appointment.appointment_date == today:
            appointment.status = "Today"
        else:
            appointment.status = "Upcoming"

    upcoming_appointments = appointments.filter(
        appointment_date__gte=today
    ).count()

    # Medical Records
    records = MedicalRecord.objects.filter(
        user=request.user
    ).order_by("-record_date")

    # Prescriptions assigned to the logged-in patient
    prescriptions = Prescription.objects.filter(
        patient=request.user
    ).select_related(
        "doctor"
    ).order_by("-created_at")

    return render(
        request,
        "accounts/dashboard.html",
        {
            "medicines": medicines,
            "medicine_count": medicines.count(),

            "appointments": appointments,
            "appointment_count": appointments.count(),
            "upcoming_appointment_count": upcoming_appointments,

            "records": records,
            "record_count": records.count(),

            "prescriptions": prescriptions,
            "prescription_count": prescriptions.count(),
        }
    )


@login_required
def doctor_dashboard(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "PATIENT"}
    )

    if profile.role != "DOCTOR":
        return redirect("dashboard")

    return render(
        request,
        "accounts/doctor_dashboard.html"
    )

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={"role": "PATIENT"}
            )

            if profile.role == "DOCTOR":
                return redirect("doctor_dashboard")

            return redirect("dashboard")

        return render(
            request,
            "accounts/login.html",
            {"error": "Invalid username or password"}
        )

    return render(request, "accounts/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")

@login_required
def profile(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()

        if not email:
            messages.error(request, "Please enter your email address.")
            return redirect("profile")

        request.user.email = email
        request.user.save(update_fields=["email"])

        messages.success(request, "Your profile has been updated successfully!")
        return redirect("profile")

    return render(request, "accounts/profile.html")
@login_required
def doctor_patients(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "PATIENT"}
    )

    if profile.role != "DOCTOR":
        return redirect("dashboard")

    patients = User.objects.filter(
        profile__role="PATIENT"
    ).select_related("profile").order_by("username")

    return render(
        request,
        "accounts/doctor_patients.html",
        {"patients": patients}
    )