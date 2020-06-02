from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager as DjangoBaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from api.models import Participant


class BaseUserManager(DjangoBaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class AppUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    delivery_at = models.DateTimeField(default=(timezone.now() - timezone.timedelta(days=10)))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = BaseUserManager()

    def __str__(self):
        return self.email


@receiver(post_save, sender=AppUser)
def post_save(sender, instance, created, **kwargs):
    if created:
        Participant.objects.create(
            name='{} {}'.format(instance.first_name, instance.last_name).strip(),
            user=instance
        )
    else:
        if not instance.participant.name.strip():
            instance.participant.name = '{} {}'.format(instance.first_name, instance.last_name).strip()
            instance.participant.save()