from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('mine/', views.my_appointments, name='patient_appointments'),
    path('<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),

    path('doctor/patients/', views.my_patients, name='doctor_patients'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
]
