from django import forms
from adminapp.models import Appointment
from .models import Prescription

class DoctorAppoinmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields=['status']



class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'
