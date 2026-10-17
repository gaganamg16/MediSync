from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .models import Medicine, Prescription
from .forms import PrescriptionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Medicine


@login_required
def medicine_list(request):
    medicines = Medicine.objects.filter(
        user=request.user
    ).order_by("reminder_time")

    now = timezone.localtime()
    today = now.date()
    current_time = now.time().replace(tzinfo=None)

    for medicine in medicines:
        if medicine.end_date < today:
            medicine.reminder_status = "Completed"
        elif medicine.start_date > today:
            medicine.reminder_status = "Upcoming"
        elif (
            current_time.hour == medicine.reminder_time.hour
            and current_time.minute == medicine.reminder_time.minute
        ):
            medicine.reminder_status = "Due now"
        elif current_time > medicine.reminder_time:
            medicine.reminder_status = "Time passed"
        else:
            medicine.reminder_status = "Upcoming"

    return render(
        request,
        "medicines/medicine_list.html",
        {"medicines": medicines}
    )


@login_required
def medicine_reminders(request):
    medicines = Medicine.objects.filter(
        user=request.user
    ).order_by("reminder_time")

    now = timezone.localtime()
    today = now.date()
    current_time = now.time().replace(tzinfo=None)

    reminders = []

    for medicine in medicines:
        if today < medicine.start_date:
            status = "Upcoming"
        elif today > medicine.end_date:
            status = "Completed"
        elif (
            current_time.hour == medicine.reminder_time.hour
            and current_time.minute == medicine.reminder_time.minute
        ):
            status = "Due now"
        elif current_time < medicine.reminder_time:
            status = "Upcoming"
        else:
            status = "Time passed"

        reminders.append({
            "medicine": medicine,
            "status": status,
        })

    return render(
        request,
        "medicines/reminders.html",
        {
            "reminders": reminders,
            "current_date": today,
            "current_time": current_time,
        },
    )


@login_required
def add_medicine(request):
    if request.method == "POST":
        Medicine.objects.create(
            user=request.user,
            name=request.POST["name"],
            dosage=request.POST["dosage"],
            instructions=request.POST.get("instructions", ""),
            start_date=request.POST["start_date"],
            end_date=request.POST["end_date"],
            reminder_time=request.POST["reminder_time"],
        )

        messages.success(request, "Medicine added successfully!")
        return redirect("medicine_list")

    return render(request, "medicines/add_medicine.html")

@login_required
def edit_medicine(request, id):
    medicine = get_object_or_404(
        Medicine,
        id=id,
        user=request.user,
    )

    if request.method == "POST":
        medicine.name = request.POST["name"]
        medicine.dosage = request.POST["dosage"]
        medicine.instructions = request.POST.get("instructions", "")
        medicine.start_date = request.POST["start_date"]
        medicine.end_date = request.POST["end_date"]
        medicine.reminder_time = request.POST["reminder_time"]

        medicine.save()

        messages.success(request, "Medicine updated successfully!")
        return redirect("medicine_list")

    return render(
        request,
        "medicines/edit_medicine.html",
        {"medicine": medicine},
    )

@login_required
def delete_medicine(request, id):
    medicine = get_object_or_404(
        Medicine,
        id=id,
        user=request.user,
    )

    if request.method == "POST":
        medicine.delete()
        messages.success(request, "Medicine deleted successfully!")
        return redirect("medicine_list")

    return render(
        request,
        "medicines/delete_medicine.html",
        {"medicine": medicine},
    )


@login_required
def add_prescription(request):
    profile = getattr(request.user, "profile", None)

    if not profile or profile.role != "DOCTOR":
        raise PermissionDenied("Only doctors can create prescriptions.")

    form = PrescriptionForm(request.POST or None)
    form.fields["patient"].queryset = User.objects.filter(
        profile__role="PATIENT"
    ).order_by("username")

    if request.method == "POST" and form.is_valid():
        prescription = form.save(commit=False)
        prescription.doctor = request.user

        prescription.save()

        messages.success(request, "Prescription created successfully!")
        return redirect("prescription_list")

    return render(
        request,
        "medicines/add_prescription.html",
        {"form": form},
    )


@login_required
def prescription_list(request):
    profile = getattr(request.user, "profile", None)

    if not profile:
        raise PermissionDenied("Your account profile is missing.")

    if profile.role == "DOCTOR":
        prescriptions = Prescription.objects.filter(
            doctor=request.user
        ).select_related("patient").order_by("-created_at")

    elif profile.role == "PATIENT":
        prescriptions = Prescription.objects.filter(
            patient=request.user
        ).select_related("doctor").order_by("-created_at")

    else:
        raise PermissionDenied(
            "This page is not available for your account."
        )

    return render(
        request,
        "medicines/prescription_list.html",
        {"prescriptions": prescriptions},
    )