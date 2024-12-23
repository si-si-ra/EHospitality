from django.db import models

# Create your models here.

class LoginTable(models.Model):
  USER_TYPES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    ]
  username=models.CharField(max_length=200)
  email=models.EmailField(max_length=200)
  password=models.CharField(max_length=200)
  cpassword=models.CharField(max_length=200)
  type = models.CharField(max_length=200, choices=USER_TYPES)

  def __str__(self):
    return '{}'.format(self.username)