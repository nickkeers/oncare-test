from django.db import models

"""
Schedule visit structure:
{
    "start_date_time": "2023-06-26T23:00:00.000Z",
    "end_date_time": "2023-06-27T22:59:59.999Z",
    "client": 1,
    "carer": 1
}
"""


class ScheduleVisit(models.Model):
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    client = models.IntegerField()
    carer = models.IntegerField()
    revision = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)