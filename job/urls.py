from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompanyProfileViewSet, JobViewSet, ApplicationViewSet, ConnectionViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'company-profiles', CompanyProfileViewSet, basename='companyprofile')
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'connections', ConnectionViewSet, basename='connection')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
]
