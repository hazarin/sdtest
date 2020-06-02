from rest_framework import permissions
from rest_framework.permissions import BasePermission
from api.models import Participant


class IsAdminOrOwner(BasePermission):
    """
    Allows write access only to superusers and owners for Participant objects.
    """

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Participant):
            if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
                return True
            else:
                return obj.user == request.user

        return True
