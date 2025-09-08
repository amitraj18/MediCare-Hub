from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    starts_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appt {self.pk} patient={self.patient} doctor={self.doctor} at {self.starts_at}"

    def clean(self):
        try:
            if getattr(self.patient, 'role', None) != 'PATIENT':
                raise ValueError('Patient must have role PATIENT')
            if getattr(self.doctor, 'role', None) != 'DOCTOR':
                raise ValueError('Doctor must have role DOCTOR')
        except Exception:
            pass
