from rest_framework.permissions import BasePermission


class IsTaskOwner(BasePermission):
    """
    Only task owner can modify task state
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user