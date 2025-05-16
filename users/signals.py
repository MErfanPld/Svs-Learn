from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from cart.models import Cart

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_cart_for_user(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
