from django.shortcuts import render,get_object_or_404,redirect
from adminapp.models import Appointment,Doctor, Patient
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage

from adminapp.forms import DoctorForm
from patient.models import MedicalHistory
from .models import Prescription
from .forms import DoctorAppoinmentForm
from datetime import datetime

def doctor_dashboard(request):
    doctor_id = request.session.get('doctor_id')

    if not doctor_id:
        messages.error(request, 'No doctor found in session. Please log in again.')
        return redirect('login')

    try:
        doctor = Doctor.objects.get(id=doctor_id)

        # Get today's appointments
        today = datetime.now().date()
        todays_appointments = Appointment.objects.filter(
            doctor=doctor,
            scheduled_date__date=today,
            status__in=['scheduled', 'rescheduled']  # Optional: Filter by specific statuses
        )

    except Doctor.DoesNotExist:
        messages.error(request, 'Doctor not found. Please contact the admin.')
        return redirect('login')

    context = {
        'doctor': doctor,
        'todays_appointments': todays_appointments,
    }
    return render(request, 'doctor/dashboard.html', context)


def doctor_details(request,doctor_id):  #particular element viewing
     doctor=Doctor.objects.get(id=doctor_id)
     return render (request,'doctor/doctor_details.html',{'doctor':doctor})


def edit_doctor(request,doctor_id):
     doctor=Doctor.objects.get(id=doctor_id)
     if request.method=='POST':
          form=DoctorForm(request.POST,request.FILES,instance=doctor)
          if form.is_valid():
               form.save()
               return redirect('doctor_details', doctor_id=doctor_id)
     else:
          form=DoctorForm(instance=doctor)
          return render(request,'doctor/edit_doctor.html',{'form':form,'doctor': doctor})
     



def doctor_appointments(request, doctor_id):
    search_query = request.GET.get('search', '')
    # Get the doctor using the doctor_id parameter
    doctor = get_object_or_404(Doctor, id=doctor_id) 
    appointments = Appointment.objects.filter(doctor=doctor,patient_name__icontains=search_query).select_related('department').order_by('-scheduled_date')
    paginator=Paginator(appointments,4)
    page_number=request.GET.get('page')
    try:
            page=paginator.get_page(page_number)
    except EmptyPage:
            page=paginator.page(page_number.num_pages)
    return render(request, 'doctor/appointment_list.html', {'appointments': appointments,'page':page,'doctor': doctor,'search_query': search_query})



def update_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    doctor = appointment.doctor  # Get the doctor object associated with the appointment
    doctor_id = doctor.id  # Get the doctor's ID
    if request.method == 'POST':
        form = DoctorAppoinmentForm(request.POST, request.FILES, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('doctor_appointments',doctor_id=doctor_id)  # Redirect to the department list after editing
    else:
        form = DoctorAppoinmentForm(instance=appointment)
    return render(request, 'doctor/update_appointment.html', {'form': form,'doctor': doctor})





def patient_list(request, doctor_id):

    search_query = request.GET.get('search', '')

    # Retrieve the Doctor object using the provided ID
    doctor = get_object_or_404(Doctor, id=doctor_id)

    # Fetch appointments for this doctor
    appointments = Appointment.objects.filter(doctor=doctor, patient_name__icontains=search_query).order_by('-scheduled_date')
    
    paginator=Paginator(appointments,4)
    page_number=request.GET.get('page')
    try:
            page=paginator.get_page(page_number)
    except EmptyPage:
            page=paginator.page(page_number.num_pages)
    # Extract the unique patient details (name, email, phone) from the appointments
    patients = [
        {
            'id': appointment.id,
            'name': appointment.patient_name,
            'phone': appointment.patient_phone,
            'email': appointment.patient_email
        }
        for appointment in appointments
    ]

    return render(request, 'doctor/patient_list.html', {'doctor': doctor, 'patients': patients,'page':page,'search_query': search_query})



def patient_details(request, patient_id, doctor_id):
    patient = get_object_or_404(Patient, id=patient_id)
    doctor = get_object_or_404(Doctor, id=doctor_id)
    medical_histories = MedicalHistory.objects.filter(patient=patient)
    context = {
        'doctor': doctor,
        'patient': patient,
        'medical_histories': medical_histories,
    }
    return render(request, 'doctor/patient_profile.html', context)





from .forms import PrescriptionForm

def add_prescription(request, doctor_id, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    # Now you can access the doctor by its ID
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.patient_name = appointment.patient_name
            prescription.doctor = doctor  # Assign the doctor to the prescription
            prescription.save()
            return redirect('doctor_appointments', doctor_id=doctor.id)  # Redirect with doctor ID
    else:
        form = PrescriptionForm()

    return render(request, 'doctor/add_prescription.html', {'form': form, 'appointment': appointment,'doctor': doctor})



def view_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    doctor = prescription.appointment.doctor  # Assuming prescription is linked to appointment, which has a doctor
    doctor_id = doctor.id  # Get the doctor ID

    return render(request, 'doctor/view_prescription.html', {
        'prescription': prescription,
        'doctor': doctor,
        'doctor_id': doctor_id  # Pass the doctor_id to the template
    })



def edit_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    doctor = prescription.appointment.doctor
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            return redirect('doctor_appointments', doctor_id=prescription.appointment.doctor.id)
    else:
        form = PrescriptionForm(instance=prescription)

    return render(request, 'doctor/edit_prescription.html', {'form': form, 'prescription': prescription, 'doctor': doctor})


def delete_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    doctor = prescription.appointment.doctor
    if request.method == 'POST':
        prescription.delete()
        return redirect('doctor_appointments', doctor_id=prescription.appointment.doctor.id)

    return render(request, 'doctor/delete_prescription.html', {'prescription': prescription, 'doctor': doctor})
