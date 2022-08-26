from rest_framework import permissions


class CustomAdminPermission(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.status == 1:
            return True
