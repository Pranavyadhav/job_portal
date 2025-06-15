from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Job, Application, CompanyProfile, Connection, Message
from .serializers import (
    JobSerializer, ApplicationSerializer, CompanyProfileSerializer,
    ConnectionSerializer, MessageSerializer
)

from user_details.permissions import IsAdminOrSuperAdmin

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)


class JobApplyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        if request.user.role != 'jobseeker':
            return Response({"error": "Only jobseekers can apply."}, status=403)

        application = Application.objects.create(
            job=job,
            applicant=request.user,
            resume_url=request.data.get("resume_url", ""),
            cover_letter=request.data.get("cover_letter", ""),
            status="pending"
        )
        return Response(ApplicationSerializer(application).data, status=201)

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
        elif user.role == 'super_admin':
            return Application.objects.all()
        return Application.objects.none()


class CompanyProfileViewSet(viewsets.ModelViewSet):
    queryset = CompanyProfile.objects.all()
    serializer_class = CompanyProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ConnectionRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        target_id = request.data.get('user_id')
        if not target_id:
            return Response({"error": "user_id is required"}, status=400)
        if Connection.objects.filter(user1=request.user.id, user2=target_id).exists():
            return Response({"message": "Connection request already sent"}, status=409)
        connection = Connection.objects.create(user1=request.user, user2_id=target_id, status='pending')
        return Response(ConnectionSerializer(connection).data, status=201)


class ConnectionAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        conn_id = request.data.get('connection_id')
        conn = get_object_or_404(Connection, id=conn_id, user2=request.user)
        conn.status = 'accepted'
        conn.save()
        return Response(ConnectionSerializer(conn).data)


class ConnectionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        connections = Connection.objects.filter(Q(user1_id=user_id) | Q(user2_id=user_id))
        return Response(ConnectionSerializer(connections, many=True).data)


class ConnectionDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        conn = get_object_or_404(Connection, id=pk)
        if request.user != conn.user1 and request.user != conn.user2:
            return Response({'error': 'You are not authorized'}, status=403)
        conn.delete()
        return Response({'status': 'Connection deleted'}, status=204)


# -------------------------
# MESSAGES
# -------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(receiver=user))


class MessageListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        messages = Message.objects.filter(
            (Q(sender=request.user) & Q(receiver_id=user_id)) |
            (Q(receiver=request.user) & Q(sender_id=user_id))
        ).order_by('id')
        return Response(MessageSerializer(messages, many=True).data)
