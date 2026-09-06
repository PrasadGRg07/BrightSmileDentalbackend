from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from .models import User, Service, Appointment, MedicalRecord
from .serializers import UserSerializer, ServiceSerializer, AppointmentSerializer, MedicalRecordSerializer

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    data = request.data
    try:
        user = User.objects.create(
            username=data['username'],
            email=data['email'],
            password=make_password(data['password']),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            phone_number=data.get('phone_number', '')
        )
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Allow anyone to list Dentists
        if self.action == 'list' and self.request.query_params.get('role') == 'Dentist':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # If filtering by Dentist, allow everyone to see them
        role_param = self.request.query_params.get('role')
        if role_param == 'Dentist':
            return User.objects.filter(role='Dentist')
            
        # Otherwise, restrict to own profile or Admin
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()
            
        if user.role == 'Admin':
            return User.objects.all()
        return User.objects.filter(id=user.id)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny] # Anyone can see services, only admins should edit (implied for MVP)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Patient':
            return Appointment.objects.filter(patient=user)
        elif user.role == 'Dentist':
            return Appointment.objects.filter(dentist=user)
        return Appointment.objects.all() # Admin/Receptionist sees all

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Patient':
            return MedicalRecord.objects.filter(patient=user)
        elif user.role == 'Dentist':
            return MedicalRecord.objects.filter(dentist=user)
        return MedicalRecord.objects.all()

    def perform_create(self, serializer):
        serializer.save(dentist=self.request.user)
