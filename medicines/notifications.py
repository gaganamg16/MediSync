from django.conf import settings
from django.core.mail import send_mail
from django.db import IntegrityError, transaction
from django.utils import timezone

from .models import Medicine, MedicineReminderLog


def send_medicine_reminders():
    """Send scheduled medicine reminder emails without duplicate daily logs."""

    now = timezone.localtime()
    today = now.date()
    current_time = now.time().replace(tzinfo=None)

    medicines = Medicine.objects.filter(
        start_date__lte=today,
        end_date__gte=today,
        reminder_time__hour=current_time.hour,
        reminder_time__minute=current_time.minute,
    ).select_related("user")

    sent_count = 0

    for medicine in medicines:
        email = medicine.user.email

        if not email:
            continue

        # Reserve today's reminder log before sending.
        try:
            with transaction.atomic():
                MedicineReminderLog.objects.create(
                    medicine=medicine,
                    reminder_date=today,
                )
        except IntegrityError:
            # A reminder log already exists for this medicine today.
            continue

        subject = f"MediSync Medicine Reminder: {medicine.name}"

        message = (
            f"Hello {medicine.user.username},\n\n"
            "This is a reminder from your MediSync medicine schedule.\n\n"
            f"Medicine: {medicine.name}\n"
            f"Dosage: {medicine.dosage}\n"
            f"Instructions: {medicine.instructions or 'Follow your prescribed instructions.'}\n"
            f"Scheduled time: {medicine.reminder_time.strftime('%I:%M %p')}\n\n"
            "Please follow the schedule provided by your healthcare professional.\n\n"
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
            # Remove the reservation if the email backend raises an error.
            MedicineReminderLog.objects.filter(
                medicine=medicine,
                reminder_date=today,
            ).delete()
            raise

        sent_count += 1

    return sent_count