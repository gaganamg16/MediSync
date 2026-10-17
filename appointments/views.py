from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Appointment

@login_required
def appointment_list(request):

    appointments = Appointment.objects.filter(
        user=request.user
    ).order_by(
        "appointment_date",
        "appointment_time"
    )

    from datetime import date

    today = date.today()

    for appointment in appointments:

        if appointment.appointment_date < today:
            appointment.status = "Completed"
        elif appointment.appointment_date == today:
            appointment.status = "Today"
        else:
            appointment.status = "Upcoming"

    return render(
        request,
        "appointments/appointment_list.html",
        {
            "appointments": appointments
        }
    )


@login_required
def add_appointment(request):

    if request.method == "POST":

        Appointment.objects.create(
            user=request.user,
            doctor_name=request.POST["doctor_name"],
            hospital_name=request.POST["hospital_name"],
            appointment_date=request.POST["appointment_date"],
            appointment_time=request.POST["appointment_time"],
            notes=request.POST["notes"],
        )

        return redirect("appointment_list")

    return render(
        request,
        "appointments/add_appointment.html"
    )


@login_required
def edit_appointment(request, id):

    appointment = get_object_or_404(
        Appointment,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        appointment.doctor_name = request.POST["doctor_name"]
        appointment.hospital_name = request.POST["hospital_name"]
        appointment.appointment_date = request.POST["appointment_date"]
        appointment.appointment_time = request.POST["appointment_time"]
        appointment.notes = request.POST["notes"]

        appointment.save()

        return redirect("appointment_list")

    return render(
        request,
        "appointments/edit_appointment.html",
        {"appointment": appointment}
    )


@login_required
def delete_appointment(request, id):

    appointment = get_object_or_404(
        Appointment,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        appointment.delete()

        return redirect("appointment_list")

    return render(
        request,
        "appointments/delete_appointment.html",
        {"appointment": appointment}
    )