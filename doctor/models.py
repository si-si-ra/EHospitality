from django.db import models

class Prescription(models.Model):
    appointment = models.OneToOneField(
        'adminapp.Appointment',  # Use the full app label for the related model
        on_delete=models.CASCADE
    )
    patient_name = models.CharField(max_length=255)
    disease = models.CharField(max_length=255)
    medication = models.TextField()
    test_needed=models.TextField()
    next_consultation_date=models.DateField()
    medical_tips = models.TextField()
    

    def __str__(self):
        return f"Prescription for {self.patient_name}"
