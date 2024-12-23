from django import forms
from adminapp.models import Appointment,Doctor
from .models import MedicalHistory


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient_name', 'patient_email', 'patient_phone', 'department', 'doctor', 'message']
    
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all(),required=True, label="Select Doctor")
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Additional message (optional)'}), required=False)

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model=MedicalHistory
        fields='__all__'
   
