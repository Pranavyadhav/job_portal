from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrSuperAdmin(BasePermission):
    """
    ✅ Allows:
    - Owners to fully manage their own data
    - Admins to READ and DELETE jobseeker data
    - Superadmins can do anything
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Resolve user from object or object.profile
        obj_user = getattr(obj, 'user', None)
        if not obj_user and hasattr(obj, 'profile'):
            obj_user = getattr(obj.profile, 'user', None)

        if not obj_user:
            return False  # Deny if we can't resolve user

        if user.role == 'super_admin':
            return True

        if user.role == 'admin':
            # Admins can read or delete jobseeker data
            if request.method in SAFE_METHODS or request.method == 'DELETE':
                return getattr(obj_user, 'role', None) == 'jobseeker'

        # Jobseeker can act only on their own data
        return obj_user == user


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

class IsNotificationOwnerOrAdmin(BasePermission):
    """
    ✅ Jobseeker can only view their own notifications
    ✅ Admins & Superadmins can create, update, delete notifications
    """
    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role in ['admin', 'super_admin']:
            return True  # Full access for admins

        if request.method in SAFE_METHODS:
            return obj.user == user  # Jobseeker can view their own only

        return False  # Jobseeker cannot update/delete