from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JobViewSet, ApplicationViewSet, CompanyProfileViewSet,
    MessageViewSet,
    JobApplyView,
    ConnectionRequestView, ConnectionAcceptView,
    ConnectionListView, ConnectionDeleteView,
    MessageListView
)

router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'applications', ApplicationViewSet)
router.register(r'company', CompanyProfileViewSet, basename='company')
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('jobs/<int:pk>/apply/', JobApplyView.as_view(), name='apply-to-job'),
    path('connections/request/', ConnectionRequestView.as_view(), name='connection-request'),
    path('connections/accept/', ConnectionAcceptView.as_view(), name='connection-accept'),
    path('connections/<int:user_id>/', ConnectionListView.as_view(), name='connection-list'),
    path('connections/<int:pk>/delete/', ConnectionDeleteView.as_view(), name='connection-delete'),
    path('messages/<int:user_id>/', MessageListView.as_view(), name='message-thread'),
    path('', include(router.urls)),  # <-- ✅ DRF API root for job endpoints
]
