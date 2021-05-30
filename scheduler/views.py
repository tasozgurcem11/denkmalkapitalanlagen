from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from scheduler import forms
from scheduler.models import *
from scheduler.helpers import weeks as weeks_helper

from datetime import timedelta, date, datetime, time
import pytz


# Create your views here.
def slot_view(request, id=None):
    request.session['slot_id'] = id
    try:
        slot_week = Slot.objects.filter(id=id)[0].week
        start_date = slot_week.start_date
    except IndexError:
        return redirect("scheduler:schedule")
    form = forms.CustomerGetSlot()

    context = {"form": form, "start_date": start_date}
    return render(request, "scheduler/slot_detail.html", context)


def schedule_view(request):
    weeks = Week.objects.all()
    if not weeks:
        messages.error(request, "Noch keine Wochen definiert! Bitte warnen Sie die Admins.")
        str_times = []
        slots_dict = {"Montag": None, "Dienstag": None,
                      "Mittwoch": None, "Donnerstag": None,
                      "Freitag": None, "Samstag": None,
                      "Sonntag": None}
        context = {"slots_dict": slots_dict, "times": str_times, "successful_submit": False}
        return render(request, "scheduler/schedule.html", context=context)
    else:
        start_dates = weeks_helper.get_start_dates_of_weeks()
        return redirect("scheduler:week", start_date=start_dates[0])


def week_view(request, start_date):
    try:
        start_dates = weeks_helper.get_start_dates_of_weeks()
    except KeyError:
        return redirect("scheduler:schedule")

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        week_index = start_dates.index(start_date)
    except ValueError:
        # It takes balls this trigger this exception, good job
        return redirect("scheduler:schedule")

    if week_index == 0:
        prev_week_start_date = None
    else:
        prev_week_start_date = start_dates[week_index - 1]
    if week_index + 1 == len(start_dates):
        next_week_start_date = None
    else:
        next_week_start_date = start_dates[week_index + 1]

    weeks = Week.objects.filter(start_date=start_date)
    open_days = {"monday": False, "tuesday": False,
                 "wednesday": False, "thursday": False,
                 "friday": False, "saturday": False,
                 "sunday": False}

    tz = pytz.timezone(weeks[0].timezone)
    week_start_date = weeks[0].start_date
    current_server_time = datetime.now(tz)

    schedule_start_time = time.max
    schedule_end_time = time.min
    min_interval = timedelta.max
    max_early_notice = timedelta.min
    for week in weeks:
        open_days["monday"] = open_days["monday"] or week.monday
        open_days["tuesday"] = open_days["tuesday"] or week.tuesday
        open_days["wednesday"] = open_days["wednesday"] or week.wednesday
        open_days["thursday"] = open_days["thursday"] or week.thursday
        open_days["friday"] = open_days["friday"] or week.friday
        open_days["saturday"] = open_days["saturday"] or week.saturday
        open_days["sunday"] = open_days["sunday"] or week.sunday

        if week.start_time < schedule_start_time:
            schedule_start_time = week.start_time
        if week.end_time > schedule_end_time:
            schedule_end_time = week.end_time
        if week.interval < min_interval:
            min_interval = week.interval
        if week.early_notice > max_early_notice:
            max_early_notice = week.early_notice

    # Delete the week if all slots are already expired
    if current_server_time.date() - timedelta(weeks=1) + max_early_notice >= week_start_date:
        Week.objects.filter(start_date=start_date).delete()
        return redirect("scheduler:schedule")

    start_time = tz.localize(datetime.combine(week_start_date, schedule_start_time))
    end_time = tz.localize(datetime.combine(week_start_date, schedule_end_time))
    half_interval = min_interval / 2

    str_times = []
    tmp_start_time = start_time
    while tmp_start_time <= end_time:
        str_times.append(tmp_start_time.time().strftime("%H:%M"))
        tmp_start_time += half_interval

    slots_dict = {"Montag": None, "Dienstag": None,
                  "Mittwoch": None, "Donnerstag": None,
                  "Freitag": None, "Samstag": None,
                  "Sonntag": None}
    days_german = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

    min_start_time = tz.localize(datetime.max - timedelta(days=1))
    max_end_time = tz.localize(datetime.min + timedelta(days=1))

    for index, open_day in enumerate(open_days.items()):
        day, available = open_day
        current_date = week_start_date + timedelta(days=index)
        day_german = days_german[index]
        if available:
            slots_in_day = Slot.objects.filter(date=current_date)
            slots_dict[day_german] = (slots_in_day, current_date)
            # Check if the slot is outdated or not
            for slot in slots_in_day:
                if slot.start_time < min_start_time:
                    min_start_time = slot.start_time
                if slot.end_time > max_end_time:
                    max_end_time = slot.end_time
                if slot.start_time - max_early_notice < current_server_time:
                    slot.outdated = True
                    slot.save(update_fields=["outdated"])
        else:
            slots_dict[day_german] = (None, current_date)

    if request.method == "POST":
        slot_id = request.session['slot_id']
        if slot_id:
            slot = Slot.objects.filter(id=slot_id)[0]
        else:
            return HttpResponseNotFound('<h1>Angeforderter Slot wurde nicht gefunden</h1>')

        form = forms.CustomerGetSlot(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.slot = slot

            # If same person requests another slot, make the previous ones available to everyone
            if Customer.objects.filter(email=customer.email).exists():
                previous_customers = Customer.objects.filter(email=customer.email)
                for previous_customer in previous_customers:
                    previous_slot = previous_customer.slot
                    # if the user registered a slot before
                    if previous_slot:
                        previous_slot.reserved = False
                        previous_slot.save(update_fields=["reserved"])
                        previous_customer.delete()

            customer.save()

            slot.reserved = True
            slot.save(update_fields=["reserved"])

            context = {"slots_dict": slots_dict, "times": str_times, "successful_submit": True,
                       "prev_week_start_date": prev_week_start_date,
                       "next_week_start_date": next_week_start_date,
                       "min_start_time": min_start_time, "max_end_time": max_end_time}
            return render(request, "scheduler/schedule.html", context=context)
        else:
            messages.error(request,
                           'Das von Ihnen eingereichte Formular war nicht gültig. Bitte versuchen Sie es erneut!')

    context = {"slots_dict": slots_dict, "times": str_times, "successful_submit": False,
               "prev_week_start_date": prev_week_start_date,
               "next_week_start_date": next_week_start_date,
               "min_start_time": min_start_time, "max_end_time": max_end_time}
    return render(request, "scheduler/schedule.html", context=context)
