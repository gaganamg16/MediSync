from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events

from medicines.notifications import send_medicine_reminders
from appointments.notifications import send_appointment_reminders

def start():
  scheduler = BackgroundScheduler(timezone="Asia/Kolkata")


  scheduler.add_jobstore(DjangoJobStore(), "default")

  scheduler.add_job(
    send_medicine_reminders,
    trigger="interval",
    minutes=1,
    id="medicine_reminder_job",
    replace_existing=True,
    max_instances=1,
    coalesce=True,
)

  scheduler.add_job(
    send_appointment_reminders,
    trigger="interval",
    minutes=1,
    id="appointment_reminder_job",
    replace_existing=True,
    max_instances=1,
    coalesce=True,
)

  register_events(scheduler)
  scheduler.start()

  return scheduler

