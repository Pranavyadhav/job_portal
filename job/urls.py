from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    JobViewSet, ApplicationViewSet, CompanyProfileViewSet,
    apply_to_job, application_status_update,
    employer_applications, jobseeker_applications,

    ConnectionRequestView, ConnectionAcceptView,
    ConnectionListView, ConnectionDeleteView,

    MessageViewSet, MessageListView,
)

router = DefaultRouter()
router.register(r'jobs', JobViewSet)
router.register(r'applications', ApplicationViewSet)
router.register(r'company', CompanyProfileViewSet, basename='company')
router.register(r'messages', MessageViewSet, basename='messages')

urlpatterns = [
    path('jobs/<int:pk>/apply/', apply_to_job),
    path('applications/<int:pk>/status/', application_status_update),
    path('employer/applications/', employer_applications),
    path('applications/', jobseeker_applications),

    path('connections/request/', ConnectionRequestView.as_view()),
    path('connections/accept/', ConnectionAcceptView.as_view()),
    path('connections/<int:user_id>/', ConnectionListView.as_view()),
    path('connections/<int:pk>/delete/', ConnectionDeleteView.as_view()),

    path('messages/<int:user_id>/', MessageListView.as_view()),

    path('', include(router.urls)),
]
