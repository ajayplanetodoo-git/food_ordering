from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from user_accounts.models import User
from rest_framework import status


class IsVendor(BasePermission):
    message = "You don't have permission to add menu."
    def has_permission(self, request: Request, view):

        if request.method =="POST":
            return request.user.role == User.VENDOR
        return True






