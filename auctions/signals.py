from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import AuctionList
import logging

@receiver(post_delete, sender=AuctionList)
def delete_image(sender, instance, **kwargs):
    try:
        instance.image.delete(save=False)
    except:
        logging.critical("image delete failed, file does not exist or cannot be found.")