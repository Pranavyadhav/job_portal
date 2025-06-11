from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfileViewSet, WorkExperienceViewSet, EducationViewSet,
    SkillAssessmentViewSet, NotificationViewSet,
    signup, login, logout, me,
    UserDetailView, ProfileByUserIdView
)
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .permissions import IsAdminOrSuperAdmin, IsOwnerOrSuperAdmin
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .models import User, Profile, WorkExperience, Education, SkillAssessment, Notification

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profiles')
router.register(r'work-experiences', WorkExperienceViewSet)
router.register(r'educations', EducationViewSet)
router.register(r'skill-assessments', SkillAssessmentViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('auth/signup/', signup),
    path('auth/login/', login),
    path('auth/logout/', logout),
    path('auth/me/', me),

    path('users/<int:pk>/', UserDetailView.as_view()),
    path('profiles/<int:user_id>/', ProfileByUserIdView.as_view()),

    path('', include(router.urls)),
]
