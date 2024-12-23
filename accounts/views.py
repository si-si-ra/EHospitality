from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import logout
from .models import LoginTable
from .models import  LoginTable
from adminapp.models import Doctor,Patient
    
def userRegistration(request):
    if request.method == 'POST':
        # Get the form data
        name = request.POST.get('name')
        date_of_birth = request.POST.get('date_of_birth')
        gender = request.POST.get('gender')  # Added gender field
        address = request.POST.get('address')  # Added address field
        phone_number = request.POST.get('phone_number')  # Added phone number field
        email = request.POST.get('email')  # Fixed email handling
        emergency_contact = request.POST.get('emergency_contact')  # Added emergency contact field
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Validate the form data
        if not all([name, date_of_birth, gender, address, phone_number, email, password, cpassword]):
            messages.info(request, 'Please fill in all fields')
        elif password != cpassword:
            messages.info(request, 'Passwords do not match')
        elif Patient.objects.filter(email=email).exists():
            messages.info(request, 'Email is already registered')
        else:
            # Save the Patient instance
            user_profile = Patient(
                name=name,
                date_of_birth=date_of_birth,
                gender=gender,
                address=address,
                phone_number=phone_number,
                email=email,  # Ensure email is saved
                emergency_contact=emergency_contact,
                password=password  # Ideally, you should hash passwords before saving
            )
            user_profile.save()

            # Save the LoginTable instance
            login_table = LoginTable(
                username=name,
                email=email,  # Save the email to LoginTable
                password=password,  # Ideally hash this as well
                type='patient'
            )
            login_table.save()

            messages.success(request, 'Registration successful')
            return redirect('login')

    return render(request, 'accounts/register.html')




def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user exists
        try:
            user_details = LoginTable.objects.get(username=username, password=password)
            user_type = user_details.type

            # Set session and redirect based on user type
            request.session['username'] = user_details.username
            request.session['user_type'] = user_type

            if user_type == 'doctor':
                # Fetch the corresponding Doctor object using the email
                try:
                    doctor = Doctor.objects.get(email=user_details.email)
                    request.session['doctor_id'] = doctor.id  # Save the doctor's ID in session
                    return redirect('doctor_dashboard')
                except Doctor.DoesNotExist:
                    messages.error(request, 'Doctor profile not found.')
                    return redirect('login')

            elif user_type == 'patient':
                # Fetch corresponding Patient profile
                try:
                    patient = Patient.objects.get(email=user_details.email)
                    request.session['patient_id'] = patient.id  # Save patient's ID in session
                    return redirect('patient_dashboard')
                except Patient.DoesNotExist:
                    messages.error(request, 'Patient profile not found.')
                    return redirect('login')
            elif user_type == 'admin':
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid role assigned to user')

        except LoginTable.DoesNotExist:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')


def logout_view(request):
     logout(request)
     return redirect('login')


from adminapp.models import Department ,Doctor # Assuming you have the Department model in the same app

def home(request):
    # Querying all departments
    departments = Department.objects.all()
    doctors=Doctor.objects.all()
    # Passing departments to the template
    return render(request, 'accounts/index.html', {'departments': departments,'doctors':doctors})




