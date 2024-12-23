from django.urls import path
from .import views

urlpatterns = [
path('',views.doctor_dashboard,name='doctor_dashboard'),
path('appointments/<int:doctor_id>/',views.doctor_appointments, name='doctor_appointments'),
path('patients/<int:doctor_id>/', views.patient_list, name='patient_list'),
path('update_appointment/<int:appointment_id>/', views.update_appointment, name='update_status_of_appointment'),

path('add-prescription/<int:doctor_id>/<int:appointment_id>/', views.add_prescription, name='add_prescription'),
path('prescription/edit/<int:prescription_id>/', views.edit_prescription, name='edit_prescription'),
path('prescription/delete/<int:prescription_id>/', views.delete_prescription, name='delete_prescription'),
path('prescription/view/<int:prescription_id>/', views.view_prescription, name='view_prescription'),


path('doctor_details/<int:doctor_id>/',views.doctor_details,name='doctor/doctor_details'),
path('edit_doctor/<int:doctor_id>/',views.edit_doctor,name='doctor/edit_doctor'),

path('patient_details/<int:patient_id>/<int:doctor_id>/',views.patient_details,name='doctor/patient_details'),
]
