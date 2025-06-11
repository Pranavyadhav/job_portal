from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Job, Application, CompanyProfile, Connection, Message
from .serializers import JobSerializer, ApplicationSerializer, CompanyProfileSerializer, ConnectionSerializer, MessageSerializer
from user_details.permissions import IsAdminOrSuperAdmin, IsOwnerOrSuperAdmin
from rest_framework.views import APIView
from rest_framework.response import Response    
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'jobseeker':
            return Application.objects.filter(applicant=user)
        elif user.role == 'admin':
            return Application.objects.filter(job__employer=user)
        return Application.objects.none()

class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ConnectionViewSet(viewsets.ModelViewSet):
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    permission_classes = [IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user) | Message.objects.filter(sender=self.request.user)

class JobApplyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        application = Application.objects.create(
            job=job,
            applicant=request.user,
            resume_url=request.data['resume_url'],
            cover_letter=request.data.get('cover_letter', ''),
            status='pending'
        )
        return Response(ApplicationSerializer(application).data)
