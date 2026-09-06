from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('Patient', 'Patient'),
        ('Dentist', 'Dentist'),
        ('Doctor', 'Doctor'),
        ('Receptionist', 'Receptionist'),
        ('Admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Patient')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # Doctor Profile Fields
    specialty = models.CharField(max_length=100, blank=True, null=True)
    education = models.CharField(max_length=255, blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    work_days = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField(default=30)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Needs_Reschedule', 'Needs Reschedule'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_patient')
    dentist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments_as_dentist')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True, null=True)
    # Patient contact info
    patient_name = models.CharField(max_length=150, blank=True, null=True)
    patient_phone = models.CharField(max_length=20, blank=True, null=True)
    patient_email = models.EmailField(blank=True, null=True)
    patient_address = models.TextField(blank=True, null=True)
    # Receptionist workflow
    receptionist_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.patient.username} with {self.dentist.username} on {self.date_time}"

class MedicalRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_records')
    dentist = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescription = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Record for {self.patient.username} on {self.date}"
