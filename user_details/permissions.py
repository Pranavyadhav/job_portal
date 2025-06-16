from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrSuperAdmin(BasePermission):
    """
    Allows object access to:
    ✅ The owner (jobseeker)
    ✅ Super admin (all)
    ✅ Admins can only READ jobseeker data
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        # Safely resolve the user from the object or its profile
        obj_user = getattr(obj, 'user', None)
        if not obj_user and hasattr(obj, 'profile'):
            obj_user = getattr(obj.profile, 'user', None)

        if request.method in SAFE_METHODS:
            if user.role == 'admin':
                return getattr(obj_user, 'role', None) == 'jobseeker'
            return obj_user == user or user.role == 'super_admin'

        return obj_user == user or user.role == 'super_admin'


class IsAdminOrSuperAdmin(BasePermission):
    """
    Grants full access only to admins and super_admins.
    Use this for view-level permission (no object checks).
    """
    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role in ['admin', 'super_admin']

class IsOwnerOrAdmin(BasePermission):
    """
    Grants access to:
    ✅ The owner (jobseeker)
    ✅ Admins if the target is a jobseeker
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        # Resolve target user from object
        target_user = getattr(obj, 'user', obj)
        if hasattr(target_user, 'profile'):
            target_user = target_user.profile.user

        if user.role == 'admin':
            return getattr(target_user, 'role', None) == 'jobseeker'
        return target_user == user
