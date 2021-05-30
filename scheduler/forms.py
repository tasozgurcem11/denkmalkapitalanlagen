from django import forms
from scheduler import models


class CustomerGetSlot(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ["first_name", "last_name", "email", "phone_number"]


class CustomerContactUs(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = ["first_name", "last_name", "phone_number", "email", "message"]
