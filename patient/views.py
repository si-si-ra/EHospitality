from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
import stripe
from adminapp.forms import PatientForm
from doctor.models import Prescription
from .forms import AppointmentForm,MedicalHistoryForm
from adminapp.models import Appointment, Bill, Doctor,Patient,Facility,Department
from django.contrib import messages
from .models import MedicalHistory
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import login_required




def patient_dashboard(request):
    patient_id = request.session.get('patient_id')  # Fetch the patient ID from the session

    if not patient_id:
        messages.error(request, 'No patient found in session. Please log in again.')
        return redirect('login')  # Redirect to login page if session data is missing

    try:
        # Fetch the patient
        patient = Patient.objects.get(id=patient_id)
        
        # Fetch upcoming appointments
        appointments = Appointment.objects.filter(
            patient_email=patient.email, status__in=['scheduled', 'pending']
        ).order_by('scheduled_date')

        # Fetch unpaid bills
        unpaid_bills = Bill.objects.filter(patient=patient, status='unpaid')

        # Paginate appointments
        paginator = Paginator(appointments, 5)  # Show 5 appointments per page
        page_number = request.GET.get('page')
        page_appointments = paginator.get_page(page_number)

        context = {
            'patient': patient,
            'appointments': page_appointments,
            'unpaid_bills': unpaid_bills,
        }
        return render(request, 'patient/dashboard.html', context)
    
    except Patient.DoesNotExist:
        messages.error(request, 'Patient not found. Please contact the admin.')
        return redirect('login')  # Redirect if patient doesn't exist




def book_appointment(request):
    patient_id = request.session.get('patient_id')  # Retrieve patient_id from session
    if not patient_id:
        return redirect('login')  # Redirect to login if patient_id is not in session
    
    patient = Patient.objects.get(id=patient_id)  # Fetch the patient object

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_appointment_list', patient_id=patient.id)

    else:
        form = AppointmentForm()

    return render(request, 'patient/book_appointment.html', {'form': form, 'patient': patient})


def appointment_success(request):
    return render(request, 'patient/appointment_success.html')



def patient_appointment_list(request, patient_id):
    # Get the patient object
    patient = get_object_or_404(Patient, id=patient_id)
    
    # Get the search query parameters
    search_query = request.GET.get('search', '').strip()

    # Filter appointments for the specific patient and based on search criteria
    appointments = Appointment.objects.filter(patient_email=patient.email).select_related('department').order_by('-scheduled_date')

    # Apply search filters using Q objects
    if search_query:
        appointments = appointments.filter(
            Q(department__name__icontains=search_query) |  # Search in department name
            Q(doctor__name__icontains=search_query)        # Search in doctor's name
        )
    
    # Paginate the filtered appointments (show 4 appointments per page)
    paginator = Paginator(appointments, 4)
    page_number = request.GET.get('page')  # Get the page number from GET request
    try:
        page = paginator.get_page(page_number)  # Get the correct page of results
    except EmptyPage:
        page = paginator.page(paginator.num_pages)  # If page number exceeds total pages, show last page

    # Render the template with the paginated and filtered data
    return render(request, 'patient/appointment_list.html', {
        'patient': patient,
        'appointments': page,  # Use paginated results
        'page': page,
        'search_query': search_query,  # The search query passed to the template
    })




@login_required
def patient_medical_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    medical_histories = MedicalHistory.objects.filter(patient=patient)

    # Debugging the queryset
    print("Medical Histories:", list(medical_histories))

    return render(request, 'patient/medical_history.html', {
        'medical_histories': medical_histories,
        'patient': patient  # Include patient object for template usage
    })



def create_medical_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    medical_histories = MedicalHistory.objects.filter(patient=patient)  # Fetch histories for this patient

    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            medical_history = form.save(commit=False)
            medical_history.patient = patient
            medical_history.save()
            return redirect('patient_medical_history', patient_id=patient.id)
    else:
        form = MedicalHistoryForm()

    return render(
        request,
        'patient/create_medical_history.html',
        {
            'form': form,
            'patient': patient,
            'medical_histories': medical_histories  # Pass histories to the template
        }
    )


def edit_medical_history(request, history_id,patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    medical_history = get_object_or_404(MedicalHistory, id=history_id)
    
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST, request.FILES, instance=medical_history)
        if form.is_valid():
            form.save()
            return redirect('patient_medical_history', patient_id=medical_history.patient.id)
    else:
        form = MedicalHistoryForm(instance=medical_history)

    return render(request, 'patient/edit_medical_history.html', {'form': form, 'medical_history': medical_history,'patient_id': medical_history.patient.id,'patient': patient})

     
def delete_medical_history(request, history_id,patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    medical_history = get_object_or_404(MedicalHistory, id=history_id)
    
    if request.method == 'POST':
        patient_id = medical_history.patient.id
        medical_history.delete()
        return redirect('patient_medical_history', patient_id=patient_id)

    return render(request, 'patient/delete_medical_history.html', {'medical_history': medical_history,'patient': patient})



def patient_profile(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    medical_histories = MedicalHistory.objects.filter(patient=patient)
    context = {
        'patient': patient,
        'medical_histories': medical_histories,
    }
    return render(request, 'patient/patient_profile.html', context)


def edit_patient(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_profile', patient_id=patient_id)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'patient/edit_patient.html', {'form': form,'patient': patient})



def patient_bill(request, patient_id):
    # Get the search query from the GET request, defaulting to an empty string if not provided
    search_query = request.GET.get('search', '')

    # Fetch the patient object by ID or return a 404 if not found
    patient = get_object_or_404(Patient, id=patient_id)

    # Filter appointments for the specific patient and based on search criteria
    appointments = Appointment.objects.filter(
        patient_name=patient.name,
        bill__isnull=False  # Only include appointments with a bill
    ).filter(
        Q(doctor__name__icontains=search_query) |  # Search in doctor's name
        Q(doctor__department__name__icontains=search_query) |  # Search in doctor's department name
        Q(department__name__icontains=search_query)  # Search in department name via appointment
    ).order_by('-scheduled_date')  # Order by scheduled date

    # Paginate the filtered appointments (show 4 appointments per page)
    paginator = Paginator(appointments, 4)
    page_number = request.GET.get('page')  # Get the page number from GET request
    try:
        page = paginator.get_page(page_number)  # Get the correct page of results
    except EmptyPage:
        page = paginator.page(paginator.num_pages)  # If page number exceeds total pages, show last page

    # Add bill details to each appointment (consultation fee, total bill, status, and bill ID)
    for appointment in page:  # Use paginated appointments (page instead of full appointments list)
        try:
            bill = Bill.objects.get(appointment=appointment)  # Get the bill associated with the appointment
            appointment.consultation_fee = bill.consultation_fee
            appointment.total_bill = bill.total_amount
            appointment.bill_status = bill.status
            appointment.bill_id = bill.id  # Ensure this is added for the template
        except Bill.DoesNotExist:
            appointment.consultation_fee = None
            appointment.total_bill = None
            appointment.bill_status = None
            appointment.bill_id = None  # Handle case where no bill exists for this appointment

    # Render the patient_bill template, passing in the required context
    return render(request, 'patient/patient_bill.html', {
        'appointments': page,  # Paginated appointments
        'patient': patient,  # The patient object
        'page': page,  # The paginated page of appointments
        'search_query': search_query,  # The search query passed to the template
    })


def view_bill(request, bill_id, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    bill = get_object_or_404(Bill, id=bill_id)
    total_bill = bill.calculate_total_amount()

    context = {
        'bill': bill,
        'additional_charges': bill.additional_charges.all(),
        'total_bill': total_bill,
        'patient': patient,
        'patient_id': patient.id,  # Ensure `patient_id` is passed explicitly
    }

    return render(request, 'patient/view_bill.html', context)



def download_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    # Create a response object for file download
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="bill_{bill.id}.txt"'

    # Generate bill content
    additional_charges = "\n".join([
        f"- {charge.charge_type}: {charge.amount}"  # Use charge_type and amount
        for charge in bill.additional_charges.all()
    ])
    
    content = f"""
    Bill ID: {bill.id}
    Patient: {bill.patient.name}
    Doctor: {bill.doctor.name}
    Department: {bill.department}
    Appointment ID: {bill.appointment.id}
    Consultation Fee: {bill.consultation_fee}
    Additional Charges:
    {additional_charges if additional_charges else 'None'}
    Total Amount: {bill.total_amount}
    Status: {bill.status.capitalize()}
    Created At: {bill.created_at.strftime('%Y-%m-%d %H:%M:%S')}
    """
    response.write(content)
    return response


def create_checkout_session(request, appointment_id):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Fetch the bill associated with the appointment
    bill = get_object_or_404(Bill, appointment_id=appointment_id)

    if request.method == 'POST':
        line_items = [{
            'price_data': {
                'currency': 'INR',
                'unit_amount': int(bill.total_amount * 100),  # Stripe expects the amount in paise
                'product_data': {
                    'name': f"Appointment Bill for {bill.patient.name} with Dr. {bill.doctor.name}",
                },
            },
            'quantity': 1,
        }]

        # Use absolute URLs instead of reverse
        success_url = request.build_absolute_uri(f"/patient/payment-success/{bill.patient.id}/?bill_id={bill.id}")
        cancel_url = request.build_absolute_uri(f"/patient/payment-cancel/{bill.patient.id}/?bill_id={bill.id}")

        # Create a Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return redirect(checkout_session.url, code=303)



def payment_success(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    bill_id = request.GET.get('bill_id')
    
    if bill_id:
        bill = get_object_or_404(Bill, id=bill_id)
        # Update the bill status to paid
        bill.status = 'paid'
        bill.save()
    
    return render(request, 'patient/payment_success.html', {'bill': bill, 'patient': patient})


def payment_cancel(request,patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    bill_id = request.GET.get('bill_id')
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, 'patient/payment_cancel.html', {'bill': bill,'patient': patient})



def view_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    return render(request, 'patient/view_prescription.html', {'prescription': prescription})


def download_prescription(request, prescription_id):
    prescription = get_object_or_404(Prescription, id=prescription_id)
    
    # Example: Create a simple text file for download
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename="prescription_{prescription.id}.txt"'
    
    content = f"""
    Prescription for: {prescription.patient_name}
    Disease: {prescription.disease}
    Medical Tips: {prescription.medical_tips}
    Medication: {prescription.medication}
    """
    response.write(content)
    return response




# Doctor List View
def doctor_list(request):
    search_query = request.GET.get('search', '')
    doctors = Doctor.objects.all()

    if search_query:
        doctors = doctors.filter(
            Q(name__icontains=search_query) | Q(department__name__icontains=search_query)
        )

    paginator = Paginator(doctors, 4)  # Show 4 doctors per page
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)  # Get the page object

    patient = Patient.objects.first()  # Example patient, adjust as needed

    return render(request, 'patient/doctor_list.html', {'doctors': doctors, 'page': page, 'patient': patient}) 


# Facility List View
def facility_list(request):
    search_query = request.GET.get('search', '')
    facilities = Facility.objects.all()

    if search_query:
        facilities = facilities.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        )

    paginator = Paginator(facilities, 4)  # Show 4 facilities per page
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)  # Get the page object

    patient = Patient.objects.first()  # Example patient, adjust as needed

    return render(request, 'patient/facility_list.html', {'facilities': facilities, 'page': page, 'patient': patient})

# Department List View
def department_list(request):
    search_query = request.GET.get('search', '')
    departments = Department.objects.all()

    if search_query:
        departments = departments.filter(
            Q(name__icontains=search_query)
        )

    paginator = Paginator(departments, 4)  # Show 4 departments per page
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)  # Get the page object

    patient = Patient.objects.first()  # Example patient, adjust as needed

    return render(
        request,
        'patient/department_list.html',
        {'departments': departments, 'page': page, 'patient': patient}
    )



def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        if appointment.status == 'scheduled':
            appointment.status = 'cancelled'
            appointment.save()
            messages.success(request, "Appointment canceled successfully.")
        else:
            messages.error(request, "Appointment cannot be canceled as it is not scheduled.")
    
    # Retrieve the patient ID based on email
    patient = get_object_or_404(Patient, email=appointment.patient_email)
    return redirect('patient_appointment_list', patient_id=patient.id)


def reschedule_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        new_date = request.POST.get('reschedule_date')  # Corrected name here
        if new_date:
            appointment.scheduled_date = new_date
            appointment.status = 'rescheduled'
            appointment.save()
            messages.success(request, "Appointment rescheduled successfully.")
        else:
            messages.error(request, "Please provide a new date to reschedule.")

    # Retrieve the patient ID using the patient_email field
    patient = get_object_or_404(Patient, email=appointment.patient_email)
    return redirect('patient_appointment_list', patient_id=patient.id)
