from django import forms
from .models import Doctor,Facility,Patient,Department,Appointment,AdditionalCharge,Bill

class DoctorForm(forms.ModelForm):
        class Meta:
            model = Doctor
            fields ='__all__'

class FacilityForm(forms.ModelForm):
        class Meta:
            model = Facility
            fields ='__all__'

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields='__all__'

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields='__all__'

class AppoinmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields=['scheduled_date','status']

class AdditionalChargeForm(forms.ModelForm):
    class Meta:
        model = AdditionalCharge
        fields='__all__'


