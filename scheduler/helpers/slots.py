from datetime import timedelta, date, datetime
import pytz

import scheduler.models as models


def week_previously_exists(instance):
    try:
        return models.Week.objects.filter(id=instance.id)[0]
    except IndexError:
        return None


def get_days_to_update(instance, pre_week):
    return {"monday": instance.monday and pre_week.monday,
            "tuesday": instance.tuesday and pre_week.tuesday,
            "wednesday": instance.wednesday and pre_week.wednesday,
            "thursday": instance.thursday and pre_week.thursday,
            "friday": instance.friday and pre_week.friday,
            "saturday": instance.saturday and pre_week.saturday,
            "sunday": instance.sunday and pre_week.sunday,
            }


def remove_days(instance, days_to_update, pre_week):
    pre_open_days = {"monday": pre_week.monday, "tuesday": pre_week.tuesday,
                     "wednesday": pre_week.wednesday, "thursday": pre_week.thursday,
                     "friday": pre_week.friday, "saturday": pre_week.saturday,
                     "sunday": pre_week.sunday}
    days_to_remove = {"monday": days_to_update["monday"] != pre_open_days["monday"],
                      "tuesday": days_to_update["tuesday"] != pre_open_days["tuesday"],
                      "wednesday": days_to_update["wednesday"] != pre_open_days["wednesday"],
                      "thursday": days_to_update["thursday"] != pre_open_days["thursday"],
                      "friday": days_to_update["friday"] != pre_open_days["friday"],
                      "saturday": days_to_update["saturday"] != pre_open_days["saturday"],
                      "sunday": days_to_update["sunday"] != pre_open_days["sunday"]}
    for day, to_remove in days_to_remove.items():
        if to_remove:
            models.Slot.objects.filter(day=day, reserved=False).delete()


def update_existing_days(instance, days_to_update, pre_week):
    # Delete slots that are earlier than the start time and later than the end time
    for index, day_to_update in enumerate(days_to_update.items()):
        day, to_update = day_to_update
        if to_update:
            date = instance.start_date + timedelta(days=index)
            tz = pytz.timezone(instance.timezone)
            if instance.start_time > pre_week.start_time:
                new_start_dt = tz.localize(datetime.combine(date, instance.start_time))
                models.Slot.objects.filter(day=day, start_time__lt=new_start_dt).delete()
            if instance.end_time < pre_week.end_time:
                new_end_dt = tz.localize(datetime.combine(date, instance.end_time))
                models.Slot.objects.filter(day=day, start_time__gt=new_end_dt,
                                           reserved=False).delete()


def create_all_slots_in_a_day(instance, start_dt, end_dt, date, day):
    tmp_start_dt = start_dt
    while tmp_start_dt <= end_dt:
        if not models.Slot.objects.filter(start_time=tmp_start_dt,
                                          end_time=tmp_start_dt + instance.interval,
                                          date=date).exists():
            models.Slot(week=instance, start_time=tmp_start_dt,
                        end_time=tmp_start_dt + instance.interval, date=date, day=day,
                        reserved=False, outdated=False).save()

        tmp_start_dt += instance.interval
