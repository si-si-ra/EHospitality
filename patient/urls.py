from django.urls import path
from .import views

urlpatterns = [
    path('',views.patient_dashboard,name='patient_dashboard'),
    path('book_appointment/',views.book_appointment,name='book_appointment'),
    path('appointment_success/', views.appointment_success, name='appointment_success'),
    path('appointments/<int:patient_id>', views.patient_appointment_list, name='patient_appointment_list'),
    # path('appointments/cancel/<int:appointment_id>/<int:patient_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('medical_history/<int:patient_id>/', views.patient_medical_history, name='patient_medical_history'),
    path('create/<int:patient_id>/', views.create_medical_history, name='create_medical_history'),
    path('edit/<int:history_id>/<int:patient_id>/', views.edit_medical_history, name='edit_medical_history'),
    path('delete/<int:history_id>/<int:patient_id>/', views.delete_medical_history, name='delete_medical_history'),
    
    path('patient_profile/<int:patient_id>/', views.patient_profile, name='patient_profile'),
    path('patient_bill/<int:patient_id>/', views.patient_bill, name='patient_bill'),
    path('bill/view/<int:bill_id>/', views.view_bill, name='view_bill'),

    path('checkout/<int:appointment_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('payment-success/<int:patient_id>/', views.payment_success, name='payment_success'),
    path('payment-cancel/<int:patient_id>/', views.payment_cancel, name='payment_cancel'),
    
    path('view_prescription/<int:prescription_id>/', views.view_prescription, name='view_prescription'),
    path('download_prescription/<int:prescription_id>/', views.download_prescription, name='download_prescription'),
    

    path('doctors/', views.doctor_list, name='patientapp_doctor_list'),
    path('departments/',views.department_list, name='patientapp_department_list'),
    path('facilities/', views.facility_list, name='patientapp_facility_list'),

    path('patient_edit/<int:patient_id>/', views.edit_patient, name='patient/patient_edit'),


    path('bill/view/<int:bill_id>/<int:patient_id>/', views.view_bill, name='patient_view_bill'),
    path('bill/download/<int:bill_id>/', views.download_bill, name='download_bill'),

    path('appointments/<int:appointment_id>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('appointments/<int:appointment_id>/reschedule/', views.reschedule_appointment, name='reschedule_appointment'),

    
]
