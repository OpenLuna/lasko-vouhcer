from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from jsonfield import JSONField

# Create your models here.
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=120, default='Anona Anonymous')

class Log(models.Model):
    user = models.ForeignKey(CustomUser, default=None, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    is_implicit = models.BooleanField(default=False)
    fallacies = JSONField(null=True, blank=True)
    theme = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
