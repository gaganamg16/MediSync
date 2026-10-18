from datetime import date
from django.db.models import Count
from django.db.models.functions import TruncMonth

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Profile, DoctorPatient
from medicines.models import Medicine, Prescription
from appointments.models import Appointment
from records.models import MedicalRecord


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    return render(request, "accounts/home.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not username or not email or not password:
            return render(
                request,
                "accounts/register.html",
                {"error": "Please fill in all required fields."}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "accounts/register.html",
                {"error": "This username is already taken."}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create a default patient profile.
        Profile.objects.get_or_create(
            user=user,
            defaults={"role": "PATIENT"}
        )

        login(request, user)

        return redirect("dashboard")

    return render(request, "accounts/register.html")


@login_required
def dashboard(request):
    from datetime import date

    today = date.today()

    # ------------------------------------------
    # MEDICINES
    # ------------------------------------------
    medicines = Medicine.objects.filter(
        user=request.user
    ).order_by("reminder_time")

    for medicine in medicines:
        if today < medicine.start_date:
            medicine.status = "Upcoming"
        elif today > medicine.end_date:
            medicine.status = "Completed"
        else:
            medicine.status = "Active"

    reminder_medicines = [
        {
            "id": medicine.id,
            "name": medicine.name,
            "dosage": medicine.dosage,
            "reminder_time": (
                medicine.reminder_time.strftime("%H:%M")
                if medicine.reminder_time
                else ""
            ),
            "start_date": medicine.start_date.isoformat(),
            "end_date": medicine.end_date.isoformat(),
        }
        for medicine in medicines
    ]

    # ------------------------------------------
    # APPOINTMENTS
    # ------------------------------------------
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

    appointment_count = appointments.count()

    upcoming_appointment_count = appointments.filter(
        appointment_date__gte=today
    ).count()

    # ------------------------------------------
    # MONTHLY APPOINTMENT ANALYTICS
    # Last six months, including the current month
    # ------------------------------------------
    monthly_start = today.replace(day=1)

    for _ in range(5):
        previous_month = monthly_start.month - 1
        previous_year = monthly_start.year

        if previous_month == 0:
            previous_month = 12
            previous_year -= 1

        monthly_start = monthly_start.replace(
            year=previous_year,
            month=previous_month
        )

    monthly_appointments = (
        appointments.filter(
            appointment_date__gte=monthly_start,
            appointment_date__lte=today
        )
        .annotate(
            month=TruncMonth("appointment_date")
        )
        .values("month")
        .annotate(
            total=Count("id")
        )
        .order_by("month")
    )

    monthly_appointment_data = {
        item["month"].strftime("%Y-%m"): item["total"]
        for item in monthly_appointments
    }

    monthly_labels = []
    monthly_counts = []

    month_cursor = monthly_start

    for _ in range(6):
        month_key = month_cursor.strftime("%Y-%m")

        monthly_labels.append(
            month_cursor.strftime("%b %Y")
        )

        monthly_counts.append(
            monthly_appointment_data.get(month_key, 0)
        )

        # Move to the next month.
        if month_cursor.month == 12:
            month_cursor = month_cursor.replace(
                year=month_cursor.year + 1,
                month=1
            )
        else:
            month_cursor = month_cursor.replace(
                month=month_cursor.month + 1
            )

    # ------------------------------------------
    # APPOINTMENT STATUS ANALYTICS
    # ------------------------------------------
    completed_appointments = appointments.filter(
        appointment_date__lt=today
    ).count()

    today_appointments = appointments.filter(
        appointment_date=today
    ).count()

    future_appointments = appointments.filter(
        appointment_date__gt=today
    ).count()

    appointment_status_labels = [
        "Completed",
        "Today",
        "Upcoming",
    ]

    appointment_status_counts = [
        completed_appointments,
        today_appointments,
        future_appointments,
    ]

    # ------------------------------------------
    # UPCOMING APPOINTMENT REMINDERS
    # ------------------------------------------
    upcoming_appointments = appointments.filter(
        appointment_date__gte=today
    )

    appointment_reminders = [
        {
            "id": appointment.id,
            "doctor_name": appointment.doctor_name,
            "hospital_name": appointment.hospital_name,
            "appointment_date": (
                appointment.appointment_date.isoformat()
            ),
            "appointment_time": (
                appointment.appointment_time.strftime("%H:%M")
                if appointment.appointment_time
                else ""
            ),
        }
        for appointment in upcoming_appointments
    ]

        # ------------------------------------------
    # SMART NOTIFICATIONS
    # ------------------------------------------
    from datetime import timedelta

    notifications = []

    # Medicine schedule notifications
    for medicine in medicines:
        if medicine.start_date <= today <= medicine.end_date:
            if medicine.reminder_time:
                notifications.append({
                    "type": "medicine",
                    "title": "Medicine Reminder",
                    "message": (
                        f"Your medicine {medicine.name} "
                        f"is scheduled at "
                        f"{medicine.reminder_time.strftime('%I:%M %p')}."
                    ),
                    "date": today,
                    "icon": "💊",
                })

    # Appointment notifications
    for appointment in appointments:
        days_until = (
            appointment.appointment_date - today
        ).days

        if days_until == 0:
            notifications.append({
                "type": "appointment",
                "title": "Appointment Today",
                "message": (
                    f"You have an appointment with "
                    f"{appointment.doctor_name} today."
                ),
                "date": appointment.appointment_date,
                "icon": "📅",
            })

        elif 0 < days_until <= 3:
            notifications.append({
                "type": "appointment",
                "title": "Upcoming Appointment",
                "message": (
                    f"Your appointment with "
                    f"{appointment.doctor_name} is in "
                    f"{days_until} day(s)."
                ),
                "date": appointment.appointment_date,
                "icon": "🗓️",
            })

    # Sort notifications by date
    notifications.sort(key=lambda item: item["date"])

    # ------------------------------------------
    # MEDICAL RECORDS
    # ------------------------------------------
    records = MedicalRecord.objects.filter(
        user=request.user
    ).order_by("-record_date")

    # ------------------------------------------
    # PRESCRIPTIONS
    # ------------------------------------------
    prescriptions = Prescription.objects.filter(
        patient=request.user
    ).select_related(
        "doctor"
    ).order_by("-created_at")

    # ------------------------------------------
    # DASHBOARD CONTEXT
    # ------------------------------------------
    context = {
        "today": today,

        # Medicines
        "medicines": medicines,
        "medicine_count": medicines.count(),
        "reminder_medicines": reminder_medicines,

        # Appointments
        "appointments": appointments,
        "appointment_count": appointment_count,
        "upcoming_appointment_count": upcoming_appointment_count,
        "appointment_reminders": appointment_reminders,

        "notifications": notifications,
        "notification_count": len(notifications),

        # Monthly appointment chart
        "monthly_appointment_labels": monthly_labels,
        "monthly_appointment_counts": monthly_counts,

        # Appointment status chart
        "appointment_status_labels": appointment_status_labels,
        "appointment_status_counts": appointment_status_counts,

        # Medical records
        "records": records,
        "record_count": records.count(),

        # Prescriptions
        "prescriptions": prescriptions,
        "prescription_count": prescriptions.count(),
    }

    return render(
        request,
        "accounts/dashboard.html",
        context
    )

@login_required
def doctor_dashboard(request):
    from django.utils import timezone
    from medicines.models import Prescription

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "PATIENT"}
    )

    if profile.role != "DOCTOR":
        messages.error(
            request,
            "You need a doctor account to access this page."
        )
        return redirect("dashboard")

    total_patients = User.objects.filter(
        profile__role="PATIENT"
    ).count()

    prescription_count = Prescription.objects.filter(
        doctor=request.user
    ).count()

    upcoming_appointments = Appointment.objects.filter(
        appointment_date__gte=timezone.localdate()
    ).count()

    context = {
        "total_patients": total_patients,
        "prescription_count": prescription_count,
        "upcoming_appointments": upcoming_appointments,
    }

    return render(
        request,
        "accounts/doctor_dashboard.html",
        context
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

    return render(
        request,
        "accounts/login.html"
    )


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required
def profile(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()

        if not email:
            messages.error(
                request,
                "Please enter your email address."
            )
            return redirect("profile")

        request.user.email = email
        request.user.save(update_fields=["email"])

        messages.success(
            request,
            "Your profile has been updated successfully!"
        )

        return redirect("profile")

    return render(
        request,
        "accounts/profile.html"
    )

@login_required
def doctor_patients(request):
    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={"role": "PATIENT"}
    )

    if profile.role != "DOCTOR":
        messages.error(
            request,
            "You need a doctor account to access this page."
        )
        return redirect("dashboard")

    patient_ids = DoctorPatient.objects.filter(
        doctor=request.user
    ).values_list("patient_id", flat=True)

    patients = User.objects.filter(
        id__in=patient_ids,
        profile__role="PATIENT"
    ).select_related(
        "profile"
    ).order_by("username")

    return render(
        request,
        "accounts/doctor_patients.html",
        {"patients": patients}
    )
