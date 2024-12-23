from django.urls import path
from .import views

urlpatterns=[
  path('',views.admin_dashboard,name='admin_dashboard'),


  path('doctors/', views.doctor_list, name='doctor_list'),
  path('create_doctor/',views.create_doctor,name='create_doctor'),
  path('edit_doctor/<int:doctor_id>/',views.edit_doctor,name='edit_doctor'),
  path('delete_doctor/<int:doctor_id>/',views.delete_doctor,name='delete_doctor'),
  path('doctor_details/<int:doctor_id>/',views.doctor_details,name='doctor_details'),


  path('facilities/', views.facility_list, name='facility_list'),
  path('facility/create/',views.facility_create, name='create_facility'),
  path('facility_details/<int:facility_id>/',views.facility_details,name='facility_details'),
  path('facilities_edit/<int:facility_id>/', views.edit_facility, name='facility_edit'),
  path('delete_facility/<int:facility_id>/',views.delete_facility,name='delete_facility'),


  path('patients/', views.patient_list, name='patient_list'),
  path('patient/create/',views.create_patient, name='create_patient'),
  path('patient_details/<int:patient_id>/',views.patient_details,name='patient_details'),
  path('patient_edit/<int:patient_id>/', views.edit_patient, name='patient_edit'),
  path('delete_patient/<int:patient_id>/',views.delete_patient,name='delete_patient'),

  path('departments/',views.department_list, name='department_list'),
  path('departments/add/', views.department_create, name='department_create'),
  path('departments/<int:department_id>/', views.department_details, name='department_details'),
  path('departments/<int:department_id>/edit/', views.edit_department, name='edit_department'),
  path('departments/<int:department_id>/delete/', views.delete_department, name='delete_department'),


  path('appointments/', views.appointment_list, name='appointment_list'),
  path('update_appointment/<int:appointment_id>/', views.update_appointment, name='update_appointment'),


    path('additional-charges/', views.additional_charge_list, name='additional_charge_list'),
    path('additional-charges/add/', views.add_additional_charge, name='add_additional_charge'),
    path('additional-charges/edit/<int:charge_id>/', views.edit_additional_charge, name='edit_additional_charge'),
    path('additional-charges/delete/<int:charge_id>/', views.delete_additional_charge, name='delete_additional_charge'),


  path('completed-appointments/',views.completed_appointments, name='completed_appointments'),
  path('bill_status/',views.bill_status, name='bill_status'),


  path('generate-bill/<int:appointment_id>/', views.generate_bill, name='generate_bill'),
  

  path('bill/view/<int:bill_id>/', views.view_bill, name='view_bill'),
  path('bill/edit/<int:bill_id>/', views.edit_bill, name='edit_bill'),

  path('department/<int:department_id>/doctors/',views.department_doctors, name='department_doctors'),

 ]