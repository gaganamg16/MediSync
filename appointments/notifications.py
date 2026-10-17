from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.utils import timezone

from .models import Appointment, AppointmentReminderLog


def send_appointment_reminders():
    """Send one email reminder for appointments scheduled for tomorrow."""

    tomorrow = timezone.localdate() + timedelta(days=1)

    appointments = Appointment.objects.filter(
        appointment_date=tomorrow
    ).select_related("user")

    sent_count = 0

    for appointment in appointments:
        email = appointment.user.email

        if not email:
            continue

        # Create a log first to prevent duplicate reminders.
        try:
            with transaction.atomic():
                AppointmentReminderLog.objects.create(
                    appointment=appointment
                )
        except IntegrityError:
            # A reminder has already been logged for this appointment.
            continue

        subject = f"MediSync Appointment Reminder: Dr. {appointment.doctor_name}"

        message = (
            f"Hello {appointment.user.username},\n\n"
            "This is a reminder about your upcoming appointment.\n\n"
            f"Doctor: {appointment.doctor_name}\n"
            f"Hospital: {appointment.hospital_name}\n"
            f"Date: {appointment.appointment_date.strftime('%d-%m-%Y')}\n"
            f"Time: {appointment.appointment_time.strftime('%I:%M %p')}\n"
            f"Notes: {appointment.notes or 'No additional notes'}\n\n"
            "Please contact the hospital if you need to change your appointment.\n\n"
            "Regards,\n"
            "MediSync"
        )

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception:
            # Allow the reminder to be retried if sending fails.
            AppointmentReminderLog.objects.filter(
                appointment=appointment
            ).delete()
            raise

        sent_count += 1

    return sent_count