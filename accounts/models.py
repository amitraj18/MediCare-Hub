from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        PATIENT = 'PATIENT', 'Patient'
        DOCTOR = 'DOCTOR', 'Doctor'
        ADMIN = 'ADMIN', 'Admin'

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.PATIENT)

    def is_patient(self):
        return self.role == self.Roles.PATIENT

    def is_doctor(self):
        return self.role == self.Roles.DOCTOR

    def is_admin(self):
        return self.role == self.Roles.ADMIN or self.is_superuser
