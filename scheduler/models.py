from datetime import timedelta, date, datetime
import pytz
from django.core.exceptions import ValidationError

from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify

from phonenumber_field.modelfields import PhoneNumberField
from scheduler.helpers import slots


# Create your models here.
class Week(models.Model):
    id = models.AutoField(primary_key=True)

    timezone = models.CharField(
        choices=[(zone, zone) for zone in pytz.common_timezones],
        max_length=32, default="Europe/Berlin"
    )

    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)

    start_date = models.DateField(
        default=date.today() + timedelta(days=-date.today().weekday(), weeks=1)
    )

    start_time = models.TimeField()
    end_time = models.TimeField()
    interval = models.DurationField(
        choices=[(timedelta(hours=1), "1 Hour"),
                 (timedelta(minutes=30), "30 Mins"),
                 ]
    )
    early_notice = models.DurationField(
        choices=[(timedelta(microseconds=0), "None"),
                 (timedelta(hours=1), "1 Hour"),
                 (timedelta(hours=2), "2 Hours"),
                 (timedelta(days=1), "1 Day"),
                 ]
    )
    slug = models.SlugField(default="", editable=False, max_length=255, null=False)

    def __str__(self):
        stringify = "Week {} | {}".format(self.id, self.start_date)
        return stringify

    def clean(self):
        if not self.start_date.weekday() == 0:
            err_msg = "Creating a week that doesn't start with Monday is not allowed!"
            raise ValidationError({"start_date": err_msg})
        if datetime.now(pytz.timezone(self.timezone)).date() - timedelta(
                weeks=1) + self.early_notice >= self.start_date:
            err_msg = "Creating a week that is a more than a week earlier today is not allowed!"
            raise ValidationError({"start_date": err_msg})

    def save(self, *args, **kwargs):
        value = self.start_date
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        kwargs = {
            "pk": self.id,
            "slug": self.slug
        }
        return reverse("scheduler:week", kwargs=kwargs)


@receiver(post_save, sender=Week, dispatch_uid="create_slots")
def create_slots(sender, instance, **kwargs):
    open_days = {"monday": instance.monday, "tuesday": instance.tuesday,
                 "wednesday": instance.wednesday, "thursday": instance.thursday,
                 "friday": instance.friday, "saturday": instance.saturday,
                 "sunday": instance.sunday}

    for index, open_day in enumerate(open_days.items()):
        day, available = open_day
        tz = pytz.timezone(instance.timezone)
        if available:
            start_dt = tz.localize(
                datetime.combine(instance.start_date + timedelta(days=index), instance.start_time))
            end_dt = tz.localize(
                datetime.combine(instance.start_date + timedelta(days=index), instance.end_time))
            date = instance.start_date + timedelta(days=index)
            slots.create_all_slots_in_a_day(instance, start_dt, end_dt, date, day)


@receiver(pre_save, sender=Week, dispatch_uid="update_slots")
def update_slots(sender, instance, **kwargs):
    pre_week = slots.week_previously_exists(instance)
    if pre_week:
        days_to_update = slots.get_days_to_update(instance, pre_week)
        slots.remove_days(instance, days_to_update, pre_week)
        slots.update_existing_days(instance, days_to_update, pre_week)


class Slot(models.Model):
    id = models.AutoField(primary_key=True)
    week = models.ForeignKey(Week, on_delete=models.CASCADE)

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    date = models.DateField()
    day = models.CharField(max_length=10, default="monday")

    reserved = models.BooleanField(default=False)
    outdated = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse("scheduler:slot_detail", kwargs={"id": self.id})

    def __str__(self):
        stringify = "{} | {:%H:%M} - {:%H:%M}".format(self.date, self.start_time, self.end_time)
        return stringify


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    slot = models.ForeignKey(Slot, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=32, default='')
    last_name = models.CharField(max_length=32, default='')
    phone_number = PhoneNumberField(region="DE")
    email = models.EmailField(default='', null=True)
    message = models.TextField(null=True)

    def __str__(self):
        if self.slot:
            stringify = "{} {} | {}".format(self.first_name, self.last_name, self.slot)
        else:
            stringify = "{} {} | Kontakt".format(self.first_name, self.last_name)
        return stringify
