from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from .models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Profile, WorkExperience, Education, SkillAssessment, Notification
from .serializers import ProfileSerializer, WorkExperienceSerializer, EducationSerializer, SkillAssessmentSerializer, NotificationSerializer
from .permissions import IsAdminOrSuperAdmin, IsOwnerOrSuperAdmin
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import RetrieveAPIView
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import User 

class UserDetailView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperAdmin]

class ProfileByUserIdView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user_id'

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    email = request.data['email']
    password = request.data['password']
    role = request.data.get('role', 'jobseeker')
    user = User.objects.create_user(email=email, password=password, role=role)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'role': user.role})

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data['email']
    password = request.data['password']
    user = authenticate(email=email, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=400)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'role': user.role})

@api_view(['POST'])
def logout(request):
    request.auth.delete()
    return Response({'status': 'Logged out'})

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'super_admin':
            return Profile.objects.all()
        elif user.role == 'admin':
            return Profile.objects.filter(user__role='jobseeker')
        return Profile.objects.filter(user=user)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def me(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

# You can copy same pattern for below ViewSets:
class WorkExperienceViewSet(viewsets.ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]

class SkillAssessmentViewSet(viewsets.ModelViewSet):
    queryset = SkillAssessment.objects.all()
    serializer_class = SkillAssessmentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSuperAdmin]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

