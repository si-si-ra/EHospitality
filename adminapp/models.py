from datetime import datetime
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Department name
    description = models.TextField(blank=True, null=True)  # Description of the department
    head = models.CharField(max_length=100, blank=True, null=True)  # Department head's name
    contact_number = models.CharField(max_length=15, blank=True, null=True)  # Contact number for the department
    location = models.CharField(max_length=200, blank=True, null=True)  # Department location within the hospital
    image = models.ImageField(upload_to='department_images/', blank=True, null=True) 
    def __str__(self):
        return self.name

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    qualification=models.CharField(max_length=255)
    department = models.ForeignKey(
        Department, 
        on_delete=models.CASCADE,  # Cascade delete doctors if the department is deleted
        related_name='doctors'  # Allows reverse lookup from Department to its Doctors
    )
    consultation_start_time = models.TimeField()
    consultation_end_time = models.TimeField()
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    email = models.EmailField(unique=True)
    address = models.TextField(max_length=500)
    phone=models.CharField(max_length=15)
    password=models.CharField(max_length=100)
    image = models.ImageField(
    upload_to='doctor_images/', 
    blank=True, 
    null=True, 
    default='doctor_images/default.jpg'  # Replace with your default image path
)

    
    def __str__(self):
        return '{}'.format(self.name)

    def consultation_hours(self):
        return f"{self.consultation_start_time} - {self.consultation_end_time}"


class Facility(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    image = models.ImageField(upload_to='facility_images/', null=True, blank=True)

    def __str__(self):
        return self.name
    


class Patient(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=gender_choices)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} "
    

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('scheduled', 'Scheduled'),
        ('rescheduled', 'rescheduled'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    patient_name = models.CharField(max_length=255)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=15)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    updated_at = models.DateTimeField(auto_now=True)  # Tracks last update timestamp
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Appointment for {self.patient_name} with Dr. {self.doctor.name}"



    
class AdditionalCharge(models.Model):
    charge_type = models.CharField(max_length=255)  # e.g., "Lab Test", "Room Charge"
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.charge_type} - ${self.amount}"


class Bill(models.Model):
     STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
    ]
     patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
     doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
     appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
     department = models.CharField(max_length=255)
     consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
     additional_charges = models.ManyToManyField(AdditionalCharge)  # Many-to-Many relationship
     total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
     created_at = models.DateTimeField(auto_now_add=True)

     def calculate_total_amount(self):
        """
        Calculate the total amount based on consultation fee and additional charges.
        """
        total_additional = sum(charge.amount for charge in self.additional_charges.all())
        return self.consultation_fee + total_additional

     def save(self, *args, **kwargs):
        if self.pk:  # Only calculate if the bill is not new
            self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)


    

