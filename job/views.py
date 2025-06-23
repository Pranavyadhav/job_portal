from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CompanyProfile, Job, Application, Connection, Message
from .serializers import CompanyProfileSerializer, JobSerializer, ApplicationSerializer, ConnectionSerializer, MessageSerializer
from .permissions import IsAdminOrReadOnly, IsJobseekerOwnerOrAdminReadOnly

class CompanyProfileViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        return CompanyProfile.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_queryset(self):
        return Job.objects.all()

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user, company_profile=CompanyProfile.objects.get(user=self.request.user))

class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsJobseekerOwnerOrAdminReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'jobseeker':
            return Application.objects.filter(applicant=user)
        if user.role == 'admin':
            return Application.objects.filter(job__employer=user)
        return Application.objects.none()

    def perform_create(self, serializer):
        serializer.save(applicant=self.request.user)

class ConnectionViewSet(viewsets.ModelViewSet):
    serializer_class = ConnectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Connection.objects.filter(user1=self.request.user) | Connection.objects.filter(user2=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user) | Message.objects.filter(receiver=self.request.user)
