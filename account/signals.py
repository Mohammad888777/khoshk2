from django.db.models.signals import post_save
from .models import User
from card.models import Cart


def autoCreateCart(sender,instance,created,**kwargs):
    if created:

        Cart.objects.create(
            card_id=str(instance.id)
        )

        
post_save.connect(autoCreateCart,sender=User)
