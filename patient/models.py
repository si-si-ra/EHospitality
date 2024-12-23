# patient/models.py

from django.db import models
from adminapp.models import Patient  # Import the Patient model from the admin app

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, related_name="medical_histories", on_delete=models.CASCADE)
    diagnosis = models.TextField(blank=True, null=True)
    diagnosis_files = models.FileField(upload_to='medical_history_files/', null=True, blank=True)
    medications = models.TextField(blank=True, null=True)
    medications_files = models.FileField(upload_to='medical_history_files/', null=True, blank=True)
    allergies = models.TextField(blank=True, null=True)
    allergies_files = models.FileField(upload_to='medical_history_files/', null=True, blank=True)
    treatment_history = models.TextField(blank=True, null=True)
    treatment_history_files = models.FileField(upload_to='medical_history_files/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical History for {self.patient.name}"


