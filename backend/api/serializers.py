from rest_framework import serializers
from .models import User, Service, Appointment, MedicalRecord

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'specialty', 'education', 'experience', 'bio', 'work_days')

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class AppointmentSerializer(serializers.ModelSerializer):
    patient_details = UserSerializer(source='patient', read_only=True)
    dentist_details = UserSerializer(source='dentist', read_only=True)
    service_details = ServiceSerializer(source='service', read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('patient',) # Patient should be inferred from the request user

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = '__all__'
        read_only_fields = ('dentist',) # Dentist should be inferred from the request user
