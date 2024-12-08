from django.db import models
from account.models import User
from .manager import CartItemManager
from core.models import Product
from jalali_date import datetime2jalali

import uuid




CART_STATUS=(
        ("paid","paid"),
        ("notPaid","notPaid")
)


SEND_STATUS=(
    ("درانتظار یافتن اولین پیک","درانتظار یافتن اولین پیک"),
    ("پیک بسته را تحویل گرفت","پیک بسته را تحویل گرفت"),
    ("بسته تحویل داده شد","بسته تحویل داده شد"),
)

class Cart(models.Model):


    is_active = models.BooleanField( 
                                        db_index = True ,
                                        verbose_name = "is active" ,
                                        help_text = "is active",
                                        default=False,
                                        null=True,
                                        blank=True

                                    )

    card_id=models.CharField(max_length=100,null=True,blank=True)

    created=models.DateTimeField(
        verbose_name="created",
        help_text="created",
        db_index=True,
        auto_now_add=True
    )

    updated=models.DateTimeField(
        verbose_name="updated",
        help_text="updated",
        db_index=True,
        auto_now=True
    )

    def __str__(self) -> str:

        return str(""+self.card_id)
    @property
    def created_irani(self):
        return datetime2jalali(self.created)
    

    class Meta:
        verbose_name ="cart"
        verbose_name_plural ="cart"
        # ordering=["updated"]
    




class CartItem(models.Model):



    user=models.ForeignKey(
        to=User,
        verbose_name="user",
        help_text="user",
        db_index=True,
        on_delete=models.CASCADE,
        null=True,
        blank=True

    )

    product=models.ForeignKey(

        to=Product,
        verbose_name="product",
        help_text="product",
        db_index=True,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    cart=models.ForeignKey(

        to=Cart,
        verbose_name="cart",
        help_text="cart",
        db_index=True,
        on_delete=models.CASCADE,
        null=True,
        blank=True

    )

    quantity = models.PositiveIntegerField(
         db_index=True,
         verbose_name="quantity",
        help_text="quantity",
    )

    is_active = models.BooleanField( 
                                        db_index = True ,
                                        verbose_name ="is_active" ,
                                        help_text ="is_active",
                                        default=False,
                                        null=True,
                                        blank=True

                                    )

    cart_status =models.CharField(

        max_length=15,
        choices=CART_STATUS,
        default="notPaid",
        verbose_name="status",
        help_text="status",
    )
        

    
    created=models.DateTimeField(
        verbose_name="created",
        help_text="created",
        db_index=True,
        auto_now_add=True
    )

    updated=models.DateTimeField(
        verbose_name="updated",
        help_text="updated",
        db_index=True,
        auto_now=True
    )

    

    objects=CartItemManager()



    @property
    def each_cart_price(self):
        return self.category.price*self.quantity
    

    @property
    def each_category_price(self):
        return self.product.price*self.quantity
    

    def __str__(self) -> str:
        return str(self.user)+"  product : "+str(self.product.name)

    @property
    def created_irani(self):
        return datetime2jalali(self.created)

    class Meta:
        verbose_name ="cart item"
        verbose_name_plural ="cart item"
        ordering=["created"]


    