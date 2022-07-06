from rest_framework import permissions, exceptions
from cinema.settings import API_SECRET_KEY


class Check_API_KEY_Auth(permissions.BasePermission):
    def has_permission(self, request, view):
        api_key_secret = request.META.get('HTTP_AUTHORIZATION')
        return api_key_secret == API_SECRET_KEY
