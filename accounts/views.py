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

    # Data used by JavaScript for medicine reminders.
    reminder_medicines = [
        {
            "id": medicine.id,
            "name": medicine.name,
            "dosage": medicine.dosage,
            "reminder_time": medicine.reminder_time.strftime("%H:%M"),
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

    upcoming_appointments = appointments.filter(
        appointment_date__gte=today
    ).count()
        # ------------------------------------------
    # MONTHLY APPOINTMENT ANALYTICS
    # ------------------------------------------
    from datetime import timedelta
    from dateutil.relativedelta import relativedelta

    current_month = today.replace(day=1)
    six_months_ago = current_month - relativedelta(months=5)

    monthly_appointments = (
        appointments.filter(
            appointment_date__gte=six_months_ago,
            appointment_date__lte=today,
        )
        .annotate(month=TruncMonth("appointment_date"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    monthly_appointment_data = {
        item["month"].strftime("%Y-%m"): item["total"]
        for item in monthly_appointments
    }

    monthly_labels = []
    monthly_counts = []

    for offset in range(6):
        month_date = (
            six_months_ago.replace(day=1)
        )

        # Move forward by the required number of months.
        month_number = month_date.month + offset
        year = month_date.year + (month_number - 1) // 12
        month = (month_number - 1) % 12 + 1
        month_date = month_date.replace(year=year, month=month)

        month_key = month_date.strftime("%Y-%m")

        monthly_labels.append(month_date.strftime("%b %Y"))
        monthly_counts.append(monthly_appointment_data.get(month_key, 0))

    # Data used by JavaScript for appointment reminders.
    appointment_reminders = [
        {
            "id": appointment.id,
            "doctor_name": appointment.doctor_name,
            "hospital_name": appointment.hospital_name,
            "appointment_date": appointment.appointment_date.isoformat(),
            "appointment_time": appointment.appointment_time.strftime("%H:%M"),
        }
        for appointment in appointments
        if appointment.appointment_date >= today
    ]

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
    # DASHBOARD
    # ------------------------------------------
    context = {
        "medicines": medicines,
        "medicine_count": medicines.count(),
        "reminder_medicines": reminder_medicines,

        "appointments": appointments,
        "appointment_count": appointments.count(),
        "upcoming_appointment_count": upcoming_appointments,
        "appointment_reminders": appointment_reminders,

                "monthly_appointment_labels": monthly_labels,
        "monthly_appointment_counts": monthly_counts,

        "records": records,
        "record_count": records.count(),

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
