from .models import StaffDetails
from django import forms

class StaffDetailsForm(forms.ModelForm):
    class Meta:
        model = StaffDetails
        fields = "__all__"