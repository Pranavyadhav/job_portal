from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user_details.views import (
    UserDetailView,
    ProfileViewSet,
    WorkExperienceViewSet,
    EducationViewSet,
    SkillAssessmentViewSet,
    signup,
    login,
    me,
    logout,
)

# 🔧 Initialize router
router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'work-experiences', WorkExperienceViewSet, basename='workexperience')
router.register(r'educations', EducationViewSet, basename='education')
router.register(r'skill-assessments', SkillAssessmentViewSet, basename='skillassessment')

# ✅ URL patterns
urlpatterns = [
    # Authentication endpoints
    path('auth/user/', UserDetailView.as_view(), name='user-detail'),
    path('auth/signup/', signup, name='signup'),
    path('auth/login/', login, name='login'),
    path('auth/me/', me, name='me'),
    path('auth/logout/', logout, name='logout'), 

    # Include router-generated URLs
    path('', include(router.urls)),
]
