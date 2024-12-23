from django.shortcuts import render,redirect,get_object_or_404
from .models import Bill, Doctor,Facility,Patient,Department,Appointment,AdditionalCharge
from django.contrib import messages
from accounts.models import LoginTable 
from .forms import *
from patient.models import MedicalHistory
from django.core.paginator import Paginator,EmptyPage
from datetime import date
from django.db.models import Q

def department_list(request):
    search_query = request.GET.get('search', '')
    departments = Department.objects.all().order_by('name')  # Explicit ordering

    if search_query:
        departments = departments.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        ).distinct()  # Use Q for combined filtering and distinct to avoid duplicates

    paginator = Paginator(departments, 4)  # 4 items per page
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)  # Simplified error handling

    return render(request, 'adminapp/department_list.html', {'departments': page.object_list, 'page': page})

# Create your views here.



def admin_dashboard(request):
    today = date.today()
    todays_appointments = Appointment.objects.filter(scheduled_date__date=today).select_related('doctor', 'department')
    return render(request,'adminapp/dashboard.html',{'todays_appointments': todays_appointments})




def doctor_list(request):
    search_query = request.GET.get('search', '')
    doctors = Doctor.objects.all()

    if search_query:
        # Apply the search filters
        doctors = doctors.filter(name__icontains=search_query) | doctors.filter(department__name__icontains=search_query)

    # Create a paginator with the filtered queryset
    paginator = Paginator(doctors, 4)
    page_number = request.GET.get('page')
    
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    # Pass the paginated doctors list and page to the template
    return render(request, 'adminapp/doctor_list.html', {'doctors': page.object_list, 'page': page})


def create_doctor(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST['name']
        qualification = request.POST['qualification']
        department_id = request.POST['department']  # Get department ID from the form
        consultation_start_time = request.POST['consultation_start_time']
        consultation_end_time = request.POST['consultation_end_time']
        consultation_fee = request.POST['consultation_fee']
        email = request.POST['email']
        address = request.POST['address']
        phone = request.POST['phone']
        password = request.POST['password']
        
        # Handle the uploaded file
        image = request.FILES.get('image')  # Retrieve the image file if provided
        
        # Fetch the corresponding Department object
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            messages.error(request, 'Selected department does not exist.')
            return redirect('create_doctor')  # Redirect back to the form

        # Create and save a Doctor instance
        doctor = Doctor.objects.create(
            name=name,
            department=department,  # Assign the Department instance
            qualification=qualification,
            consultation_start_time=consultation_start_time,
            consultation_end_time=consultation_end_time,
            consultation_fee=consultation_fee,
            email=email,
            address=address,
            phone=phone,
            password=password,
            image=image  # Assign the uploaded image
        )

        # Create a corresponding LoginTable entry for authentication
        LoginTable.objects.create(
            username=name,  # You could use name or another identifier
            email=email,
            password=password,
            cpassword=password,  # Ensure cpassword matches for now
            type='doctor'  # Set the user type as 'doctor'
        )

        messages.success(request, 'Doctor registered successfully! You can now log in.')
        return redirect('doctor_list')  # Replace with your actual dashboard URL name

    # Fetch all departments for the dropdown
    departments = Department.objects.all()
    return render(request, 'adminapp/create_doctor.html', {'departments': departments})



def doctor_details(request,doctor_id):  #particular element viewing
     doctor=Doctor.objects.get(id=doctor_id)
     return render (request,'adminapp/doctor_details.html',{'doctor':doctor})


def edit_doctor(request,doctor_id):
     doctor=Doctor.objects.get(id=doctor_id)
     if request.method=='POST':
          form=DoctorForm(request.POST,request.FILES,instance=doctor)
          if form.is_valid():
               form.save()
               return redirect('doctor_list')
     else:
          form=DoctorForm(instance=doctor)
          return render(request,'adminapp/edit_doctor.html',{'form':form})
     

def delete_doctor(request,doctor_id):
    doctor=Doctor.objects.get(id=doctor_id)
    if request.method=='POST':
          doctor.delete()
          return redirect('doctor_list')
    return render(request,'adminapp/delete_doctor.html',{'doctor':doctor})





def facility_list(request):
    search_query = request.GET.get('search', '')
    facilities = Facility.objects.all()

    # Apply search filters if query is provided
    if search_query:
        facilities = facilities.filter(name__icontains=search_query) | facilities.filter(location__icontains=search_query)

    # Apply pagination
    paginator = Paginator(facilities, 4)  # Show 4 facilities per page
    page_number = request.GET.get('page')
    
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)  # Fallback to last page if page number is out of range

    return render(request, 'adminapp/facility_list.html', {'facilities': page.object_list, 'page': page})



def facility_create(request):
    if request.method == 'POST':
        form = FacilityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('facility_list')
    else:
        form = FacilityForm()
    return render(request, 'adminapp/create_facility.html', {'form': form})


def facility_details(request,facility_id):  #particular element viewing
     facility=Facility.objects.get(id=facility_id)
     return render (request,'adminapp/facility_details.html',{'facility':facility})


def edit_facility(request,facility_id):
     facility=Facility.objects.get(id=facility_id)
     if request.method=='POST':
          form=FacilityForm(request.POST,request.FILES,instance=facility)
          if form.is_valid():
               form.save()
               return redirect('facility_list')

     else:
          form=FacilityForm(instance=facility)
          return render(request,'adminapp/edit_facility.html',{'form':form})

  
     
def delete_facility(request,facility_id):
    facility=Facility.objects.get(id=facility_id)
    if request.method=='POST':
          facility.delete()
          return redirect('facility_list')
    return render(request,'adminapp/delete_facility.html',{'facility':facility})



from django.core.paginator import Paginator, EmptyPage

def patient_list(request):
    search_query = request.GET.get('search', '')
    patients = Patient.objects.all()

    if search_query:
        patients = patients.filter(
            name__icontains=search_query
        ) | patients.filter(
            phone_number__icontains=search_query
        ) | patients.filter(
            email__icontains=search_query
        )

    paginator = Paginator(patients, 4)
    page_number = request.GET.get('page')
    
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'adminapp/patient_list.html', {'patients': page.object_list, 'page': page})



def create_patient(request):
    if request.method == 'POST':
        # Retrieve form data
        name = request.POST['name']
        date_of_birth = request.POST['date_of_birth']
        gender = request.POST['gender']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        emergency_contact = request.POST['emergency_contact']
        password = request.POST['password']

        # Create and save a Patient instance
        patient = Patient.objects.create(
            name=name,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            phone_number=phone_number,
            email=email,
            emergency_contact=emergency_contact,
            password=password
        )

        # Create a corresponding LoginTable entry for authentication
        LoginTable.objects.create(
            username=name,
            email=email,
            password=password,
            cpassword=password,  # Ensure cpassword matches for now
            type='patient'  # Set the user type as 'patient'
        )

        messages.success(request, 'Patient registered successfully! You can now log in.')
        return redirect('patient_list')  # Replace with your actual dashboard URL name

    return render(request, 'adminapp/create_patient.html')


def patient_details(request,patient_id):  #particular element viewing
      patient = get_object_or_404(Patient, id=patient_id)
      medical_histories = MedicalHistory.objects.filter(patient=patient)
      context = {
        'patient': patient,
        'medical_histories': medical_histories,
      }
      return render(request, 'adminapp/patient_profile.html', context)
    

def edit_patient(request,patient_id):
     patient=Patient.objects.get(id=patient_id)
     if request.method=='POST':
          form=PatientForm(request.POST,request.FILES,instance=patient)
          if form.is_valid():
               form.save()
               return redirect('patient_list')
     else:
          form=PatientForm(instance=patient)
          return render(request,'adminapp/edit_patient.html',{'form':form})
     

def delete_patient(request,patient_id):
    patient=Patient.objects.get(id=patient_id)
    if request.method=='POST':
          patient.delete()
          return redirect('patient_list')
    return render(request,'adminapp/delete_patient.html',{'patient':patient})




# List all departments


def department_list(request):
    search_query = request.GET.get('search', '')
    departments = Department.objects.all().order_by('name')  # Explicit ordering

    if search_query:
        departments = departments.filter(
            Q(name__icontains=search_query) | Q(location__icontains=search_query)
        ).distinct()  # Use Q for combined filtering and distinct to avoid duplicates

    paginator = Paginator(departments, 4)  # 4 items per page
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)  # Simplified error handling

    return render(request, 'adminapp/department_list.html', {'departments': page.object_list, 'page': page})


# Create a new department


def department_create(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES)  # Ensure both data and files are passed
        if form.is_valid():
            department = form.save(commit=False)
            # Optional: Additional logic for the instance
            department.save()  # Save the new instance
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'adminapp/create_department.html', {'form': form})


# View details of a particular department
def department_details(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    doctors = Doctor.objects.filter(department=department)
    return render(request, 'adminapp/department_details.html', {'department': department, 'doctors': doctors})


# Edit an existing department
def edit_department(request, department_id):
    department = Department.objects.get(id=department_id)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')  # Redirect to the department list after editing
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'adminapp/edit_department.html', {'form': form})

# Delete a department
def delete_department(request, department_id):
    department = Department.objects.get(id=department_id)
    if request.method == 'POST':
        department.delete()
        return redirect('department_list')  # Redirect to the department list after deletion
    return render(request, 'adminapp/delete_department.html', {'department': department})


def department_doctors(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    doctors = Doctor.objects.filter(department=department)
    return render(request, 'adminapp/department_doctors.html', {'department': department, 'doctors': doctors})


def appointment_list(request):
    search_query = request.GET.get('search', '')
    appointments = Appointment.objects.select_related('doctor', 'department').all()

    if search_query:
        appointments = appointments.filter(
            patient_name__icontains=search_query) | appointments.filter(
            patient_email__icontains=search_query) | appointments.filter(
            patient_phone__icontains=search_query) | appointments.filter(
            doctor__name__icontains=search_query) | appointments.filter(
            department__name__icontains=search_query)

    paginator = Paginator(appointments, 4)
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'adminapp/appointment_list.html', {'appointments': appointments, 'page': page})



def update_appointment(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    if request.method == 'POST':
        form = AppoinmentForm(request.POST, request.FILES, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')  # Redirect to the department list after editing
    else:
        form = AppoinmentForm(instance=appointment)
    return render(request, 'adminapp/update_appointment.html', {'form': form})



from django.core.paginator import Paginator, EmptyPage

def completed_appointments(request):
    search_query = request.GET.get('search', '')
    # Filter appointments with status "completed"
    appointments = Appointment.objects.filter(status="completed")
    
    if search_query:
        appointments = appointments.filter(
            patient_name__icontains=search_query
        ) | appointments.filter(
            doctor__name__icontains=search_query
        ) | appointments.filter(
            department__name__icontains=search_query
        )

    paginator = Paginator(appointments, 4)  # Paginate with 4 items per page
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        'appointments': page.object_list,  # Pass only the current page objects
        'page': page,                      # Pass the page object for controls
    }
    return render(request, 'adminapp/completed_appointments.html', context)


def additional_charge_list(request):
    search_query = request.GET.get('search', '')
    charges = AdditionalCharge.objects.all()

    if search_query:
        charges = charges.filter(
            charge_type__icontains=search_query
        ) | charges.filter(amount__icontains=search_query)  # Search by charge_type or amount

    paginator = Paginator(charges, 4)  # Paginate with 4 items per page
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    context = {
        'charges': page.object_list,  # Pass only the objects on the current page
        'page': page,                # Pass the page object for pagination controls
    }
    return render(request, 'adminapp/additional_charge_list.html', context)


def add_additional_charge(request):
    if request.method == 'POST':
        form = AdditionalChargeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('additional_charge_list')
    else:
        form = AdditionalChargeForm()

    return render(request, 'adminapp/add_additional_charge.html', {'form': form})


def edit_additional_charge(request, charge_id):
    charge = get_object_or_404(AdditionalCharge, id=charge_id)
    if request.method == 'POST':
        form = AdditionalChargeForm(request.POST, instance=charge)
        if form.is_valid():
            form.save()
            return redirect('additional_charge_list')
    else:
        form = AdditionalChargeForm(instance=charge)

    return render(request, 'adminapp/edit_additional_charge.html', {'form': form, 'charge': charge})


def delete_additional_charge(request, charge_id):
    charge = get_object_or_404(AdditionalCharge, id=charge_id)
    if request.method == 'POST':
        charge.delete()
        return redirect('additional_charge_list')
    return render(request, 'adminapp/delete_additional_charge.html', {'charge': charge})



def generate_bill(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    patient = get_object_or_404(Patient, name=appointment.patient_name)
    doctor = appointment.doctor
    department = appointment.department.name
    consultation_fee = doctor.consultation_fee

    # Fetch or create the bill for this appointment
    bill, created = Bill.objects.get_or_create(
        appointment=appointment,
        defaults={
            'patient': patient,
            'doctor': doctor,
            'department': department,
            'consultation_fee': consultation_fee,
        }
    )

    charge_amount = None
    selected_charge_id = request.GET.get('charge_type')

    if selected_charge_id:
        selected_charge = get_object_or_404(AdditionalCharge, id=selected_charge_id)
        charge_amount = selected_charge.amount

    if request.method == 'POST':
        if 'add_charge' in request.POST:
            # Add additional charge
            charge_id = request.POST.get('charge_type')
            additional_charge = get_object_or_404(AdditionalCharge, id=charge_id)
            bill.additional_charges.add(additional_charge)
            bill.save()

        elif 'remove_charge' in request.POST:
            # Remove charge
            charge_id = request.POST.get('charge_id')
            additional_charge = get_object_or_404(AdditionalCharge, id=charge_id)
            bill.additional_charges.remove(additional_charge)
            bill.save()

    total_bill = bill.calculate_total_amount()

    context = {
        'appointment': appointment,
        'bill': bill,
        'additional_charges': bill.additional_charges.all(),
        'available_charges': AdditionalCharge.objects.all(),
        'charge_amount': charge_amount,
        'selected_charge_id': selected_charge_id,
        'total_bill': total_bill,
    }

    return render(request, 'adminapp/generate_bill.html', context)


def bill_status(request):
    search_query = request.GET.get('search', '')

    # Fetch all appointments that have an associated bill and filter by search query
    appointments = Appointment.objects.filter(
        bill__isnull=False, patient_name__icontains=search_query
    ).order_by('-scheduled_date')

    paginator = Paginator(appointments, 4)
    page_number = request.GET.get('page')
    try:
        page = paginator.get_page(page_number)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    # Add total bill details for appointments in the current page
    for appointment in page.object_list:
        bill = Bill.objects.get(appointment=appointment)
        appointment.bill = bill  # Add the bill object
        appointment.consultation_fee = bill.consultation_fee
        appointment.total_bill = bill.total_amount
        appointment.bill_status = bill.status  # Add status to context

    context = {
        'appointments': page.object_list,  # Current page appointments
        'page': page,                      # Pagination metadata
    }
    return render(request, 'adminapp/bill_status.html', context)



def view_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    total_bill = bill.calculate_total_amount()

    context = {
        'bill': bill,
        'additional_charges': bill.additional_charges.all(),
        'total_bill': total_bill,
    }

    return render(request, 'adminapp/view_bill.html', context)


def edit_bill(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)

    if request.method == 'POST':
        if 'add_charge' in request.POST:
            charge_id = request.POST.get('charge_type')
            if charge_id:
                additional_charge = get_object_or_404(AdditionalCharge, id=charge_id)
                bill.additional_charges.add(additional_charge)
                bill.save()
        elif 'remove_charge' in request.POST:
            charge_id = request.POST.get('charge_id')
            if charge_id:
                additional_charge = get_object_or_404(AdditionalCharge, id=charge_id)
                bill.additional_charges.remove(additional_charge)
                bill.save()

    total_bill = bill.calculate_total_amount()

    context = {
        'bill': bill,
        'additional_charges': bill.additional_charges.all(),
        'available_charges': AdditionalCharge.objects.all(),
        'total_bill': total_bill,
    }

    return render(request, 'adminapp/edit_bill.html', context)





