from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_auth.serializers import LoginSerializer, UserDetailsSerializer, PasswordResetSerializer
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework.exceptions import NotFound
from django.utils.translation import gettext_lazy as _
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


class AppPasswordResetSerializer(PasswordResetSerializer):
    def validate_email(self, value):
        if not get_user_model().objects.filter(email=value).exists():
            raise NotFound(_('Email not found'))

        return super().validate_email(value)
