from datetime import date, datetime
import time

from scheduler.models import Week


def get_start_dates_of_weeks():
    weeks = Week.objects.all()
    start_dates = []
    earliest_date = date.max
    for week in weeks:
        if week.start_date not in start_dates:
            start_dates.append(week.start_date)
            if week.start_date < earliest_date:
                earliest_date = week.start_date

    start_dates = sorted(start_dates)
    return start_dates
