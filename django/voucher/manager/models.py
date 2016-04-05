from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import crypto

# Create your models here.
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=120, default='Anona Anonymous')

class Voucher(models.Model):
    user = models.ForeignKey(CustomUser, default=None, null=True, blank=True)
    code = models.CharField(max_length=12, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    used = models.BooleanField(default=False)
    shared = models.BooleanField(default=False)
    shared_voucher = models.ForeignKey("self", default=None, null=True, blank=True)

    @classmethod
    def create(cls):
        voucher_id = crypto.get_random_string(length=12)
        while Voucher.objects.filter(code=voucher_id):
            voucher_id = crypto.get_random_string(length=12)
        book = cls(code=voucher_id)
        book.save()
        # do something with the book
        return book


# method for updating
#@receiver(post_save, sender=CustomUser, dispatch_uid="create_voucher")
def create_voucher(sender, instance, **kwargs):
    voucher_id = crypto.get_random_string(length=12)
    while Voucher.objects.filter(code=voucher_id):
        voucher_id = crypto.get_random_string(length=12)
    Voucher(user=instance, code=voucher_id).save()