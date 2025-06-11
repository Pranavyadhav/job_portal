from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    signup, login, logout, me,
    UserDetailView, ProfileByUserIdView,
    ProfileViewSet, WorkExperienceViewSet,
    EducationViewSet, SkillAssessmentViewSet,
    NotificationViewSet
)
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet)
router.register(r'work-experiences', WorkExperienceViewSet)
router.register(r'educations', EducationViewSet)
router.register(r'skill-assessments', SkillAssessmentViewSet)
router.register(r'notifications', NotificationViewSet)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root_view(request):
    return Response(router.get_urls())


# manual endpoints + include router
urlpatterns = [
    path('auth/signup/', signup),
    path('auth/login/', login),
    path('auth/logout/', logout),
    path('auth/me/', me),
    path('users/<int:pk>/', UserDetailView.as_view()),
    path('profiles/<int:user_id>/', ProfileByUserIdView.as_view()),
    path('', include(router.urls)),  # <-- ✅ DRF API root for user endpoints
]
