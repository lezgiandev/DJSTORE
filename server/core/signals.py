from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Venue

@receiver(pre_delete, sender=Venue)
def delete_dj_files(sender, instance, **kwargs):
    if instance.qr_code:
        instance.qr_code.delete(save=False)
