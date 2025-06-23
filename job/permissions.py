from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Admins can do anything; others can only read.
    """
    def has_permission(self, request, view):
        user = request.user
        if user.role == 'admin':
            return True
        return request.method in SAFE_METHODS

class IsJobseekerOwnerOrAdminReadOnly(BasePermission):
    """
    Jobseekers can fully manage their own Applications.
    Admins can only read Applications for their jobs.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in SAFE_METHODS:
            if user.role == 'admin' and obj.job.employer == user:
                return True
            return obj.applicant == user

        return obj.applicant == user
