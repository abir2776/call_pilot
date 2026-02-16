from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "call_pilot.settings")

app = Celery("call_pilot")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


# -------------------------------
#     Celery Beat SCHEDULE
# -------------------------------
app.conf.beat_schedule = {
    # # Evening: 5 PM to 11:59 PM (Monday-Friday)
    # "run-initiate-interview-evening": {
    #     "task": "interview.tasks.ai_phone.initiate_all_interview",
    #     "schedule": crontab(minute="*/5", hour="17-23", day_of_week="1-5"),
    # },
    # # Morning: 12 AM to 8:59 AM (Tuesday-Saturday for weekdays + Monday for weekend coverage)
    # "run-initiate-interview-morning": {
    #     "task": "interview.tasks.ai_phone.initiate_all_interview",
    #     "schedule": crontab(minute="*/5", hour="0-8", day_of_week="1-6"),
    # },
    # # Weekend: All day Saturday and Sunday until Monday 9 AM
    # "run-initiate-interview-weekend": {
    #     "task": "interview.tasks.ai_phone.initiate_all_interview",
    #     "schedule": crontab(minute="*/5", hour="*", day_of_week="0,6"),
    # },
    "run-initiate-interview-evening": {
        "task": "interview.tasks.ai_phone.initiate_all_interview",
        "schedule": crontab(minute="*/5"),
    },
}
