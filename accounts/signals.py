from django.db.models.signals import post_delete
from django.dispatch import receiver
from adminapp.models import Doctor  # Import the Doctor model from the staff app
from .models import LoginTable  # Import the LoginTable model from the accounts app

@receiver(post_delete, sender=LoginTable)
def delete_related_doctor(sender, instance, **kwargs):
    try:
        # Check if the doctor exists with the matching email in the Doctor model
        doctor = Doctor.objects.get(email=instance.email)  # Match by email
        doctor.delete()  # Delete the related doctor instance
    except Doctor.DoesNotExist:
        pass  # If no related doctor is found, do nothing
