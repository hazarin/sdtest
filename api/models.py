from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class PrecedentCatalog(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Participant(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class Precedent(models.Model):
    ATTITUDE_CHOICES = [
        (0, 'negative'),
        (1, 'positive')
    ]
    precedent = models.ForeignKey(PrecedentCatalog, on_delete=models.CASCADE)
    attitude = models.PositiveSmallIntegerField(choices=ATTITUDE_CHOICES, default=1)
    importance = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    participant = models.ForeignKey(Participant, related_name='precedents', on_delete=models.CASCADE)
