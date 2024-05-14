from rest_framework import permissions
from users.models import User


class IsLibrarian(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile == User.UserProfile.LIBRARIAN

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user.profile == User.UserProfile.LIBRARIAN
