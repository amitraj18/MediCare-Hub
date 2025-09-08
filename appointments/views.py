from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import patient_required, doctor_required
from django.contrib.auth import get_user_model
from .models import Appointment
from django.utils.dateparse import parse_datetime

User = get_user_model()

@login_required
@patient_required
def book_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        starts_at = request.POST.get('starts_at')
        if not doctor_id or not starts_at:
            return render(request, 'appointments/book.html', {'error': 'Missing fields', 'doctors': User.objects.filter(role='DOCTOR')})
        doctor = get_object_or_404(User, pk=doctor_id, role='DOCTOR')
        dt = parse_datetime(starts_at)
        if not dt:
            return render(request, 'appointments/book.html', {'error': 'Invalid date format', 'doctors': User.objects.filter(role='DOCTOR')})
        Appointment.objects.create(patient=request.user, doctor=doctor, starts_at=dt)
        return redirect('patient_appointments')
    doctors = User.objects.filter(role='DOCTOR')
    return render(request, 'appointments/book.html', {'doctors': doctors})

@login_required
@patient_required
def my_appointments(request):
    qs = Appointment.objects.filter(patient=request.user).order_by('-starts_at')
    return render(request, 'appointments/patient_list.html', {'appointments': qs})

@login_required
@patient_required
def cancel_appointment(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, patient=request.user)
    if request.method == 'POST':
        appt.delete()
        return redirect('patient_appointments')
    return render(request, 'appointments/confirm_cancel.html', {'appointment': appt})

@login_required
@doctor_required
def my_patients(request):
    patient_ids = Appointment.objects.filter(doctor=request.user).values_list('patient', flat=True).distinct()
    patients = User.objects.filter(id__in=patient_ids)
    return render(request, 'appointments/doctor_list.html', {'patients': patients})

@login_required
@doctor_required
def doctor_appointments(request):
    qs = Appointment.objects.filter(doctor=request.user).select_related('patient').order_by('-starts_at')
    return render(request, 'appointments/doctor_list.html', {'appointments': qs})
