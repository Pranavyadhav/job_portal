from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User
from rest_framework import viewsets
from .models import Profile, WorkExperience, Education, SkillAssessment, Notification
from .serializers import ProfileSerializer, WorkExperienceSerializer, EducationSerializer, SkillAssessmentSerializer, NotificationSerializer
from .permissions import IsAdminOrSuperAdmin
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import RetrieveAPIView
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from django.contrib.auth import get_user_model
User = get_user_model()
from .permissions import IsOwnerOrSuperAdmin, IsOwnerOrAdmin


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    email = request.data.get('email')
    password = request.data.get('password')
    role = request.data.get('role', 'jobseeker')

    if not email or not password:
        return Response({"error": "Email and password are required."}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "User with this email already exists."}, status=409)

    user = User.objects.create_user(email=email, password=password, role=role)

    return Response({
        "message": "User registered successfully.",
        "role": user.role
    }, status=201)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password are required."}, status=400)

    user = authenticate(email=email, password=password)  # ✅ FIX: no `request`

    if user is None:
        return Response({"error": "Invalid credentials."}, status=401)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        "token": token.key,
        "role": user.role
    }, status=200)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()  # Delete the user's token
    return Response({"message": "Logged out successfully."}, status=200)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def me(request):
    return Response(UserSerializer(request.user).data)

class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Profile.objects.filter(user__role='jobseeker')
        elif user.role == 'super_admin':
            return Profile.objects.all()
        return Profile.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        if Profile.objects.filter(user=user).exists():
            raise ValidationError("You already have a profile.")
        serializer.save(user=user)

class WorkExperienceViewSet(viewsets.ModelViewSet):
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'super_admin':
            return WorkExperience.objects.all()
        return WorkExperience.objects.filter(profile__user=user)

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        if WorkExperience.objects.filter(profile=profile).exists():
            raise ValidationError("You already added work experience.")
        serializer.save(profile=profile)


class EducationViewSet(viewsets.ModelViewSet):
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'super_admin':
            return Education.objects.all()
        return Education.objects.filter(profile__user=user)

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        if WorkExperience.objects.filter(profile=profile).exists():
            raise ValidationError("You already added work experience.")
        serializer.save(profile=profile)


class SkillAssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = SkillAssessmentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'super_admin':
            return SkillAssessment.objects.all()
        return SkillAssessment.objects.filter(profile__user=user)

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        if WorkExperience.objects.filter(profile=profile).exists():
            raise ValidationError("You already added work experience.")
        serializer.save(profile=profile)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Each user sees only their own notifications
        return Notification.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Optional: auto-assign user to the notification
        serializer.save(user=self.request.user)
