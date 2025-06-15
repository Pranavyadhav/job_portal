from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrSuperAdmin(BasePermission):
    """
    ✅ Allows object access to:
    - The owner (request.user == obj.user)
    - Or super_admin
    - Admins can READ jobseeker-owned objects only
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        # Determine the object's user reference
        obj_user = getattr(obj, 'user', obj)

        if request.method in SAFE_METHODS:
            if user.role == 'admin':
                return getattr(obj_user, 'role', None) == 'jobseeker'
            return obj_user == user or user.role == 'super_admin'

        # Write methods (POST/PUT/PATCH/DELETE)
        return obj_user == user or user.role == 'super_admin'


class IsAdminOrSuperAdmin(BasePermission):
    """
    ✅ General view-level permission for admin & super_admin
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role in ['admin', 'super_admin']

class IsOwnerOrAdmin(BasePermission):
    """
    Allows jobseekers to access their own data.
    Allows admins to access jobseeker data.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        target_user = getattr(obj, 'user', obj)  # Works for both User and related models

        if user.role == 'admin':
            return getattr(target_user, 'role', None) == 'jobseeker'
        return target_user == user