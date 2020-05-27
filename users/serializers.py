from django.conf import settings
from rest_framework import serializers
from rest_auth.serializers import LoginSerializer, UserDetailsSerializer
from rest_auth.registration.serializers import RegisterSerializer
from . import models


class AppLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True, allow_blank=False)


class AppUserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = models.AppUser
        fields = ('pk', 'email', 'first_name', 'last_name')
        read_only_fields = ('email', )


class AppRegisterSerializer(RegisterSerializer):
    username = None