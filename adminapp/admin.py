# admin.py
from django.contrib import admin
from .models import Department, Doctor, Patient,Facility,Appointment,AdditionalCharge, Bill


admin.site.register(Department)
admin.site.register(Facility)
admin.site.register(Doctor)
admin.site.register(Patient)


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'doctor', 'status', 'scheduled_date', 'updated_at')
    list_filter = ('status', 'doctor', 'department')
    search_fields = ('patient_name', 'patient_email')
    list_editable = ('status',)

admin.site.register(Appointment, AppointmentAdmin)


admin.site.register(AdditionalCharge)
admin.site.register(Bill)
