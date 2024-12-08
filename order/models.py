from django.db import models
from account.models import User
from account.utils import generate_auto_custom_id
from card.models import Cart,CartItem
import uuid

from jalali_date import datetime2jalali



SEND_STATUS=(
    ("درانتظار یافتن اولین پیک","درانتظار یافتن اولین پیک"),
    ("پیک بسته را تحویل گرفت","پیک بسته را تحویل گرفت"),
    ("بسته تحویل داده شد","بسته تحویل داده شد"),
)





class Payment(models.Model):

  

    card_hash=models.CharField(
        max_length=250,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="card hash",
        help_text="card hash",
        db_column="card_hash"
    )

    card_pan=models.CharField(
        max_length=250,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="card_pan",
        help_text="card_pan",
        db_column="card_pan"
    )

    
    ref_id=models.CharField(
        max_length=250,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="ref_id",
        help_text="ref_id",
        db_column="ref_id"
    )
    

    bank_name=models.CharField(
        max_length=150,
        db_index=True,
        null=True,
        blank=True,
        db_column="bank_name",
        db_comment="bank name",
        name="bank_name",
        verbose_name="اسم بانک",
        help_text="اسم بانک",
    )


    bank_status=models.CharField(
        max_length=150,
        db_index=True,
        null=True,
        blank=True,
        db_column="bank_status",
        db_comment="bank_status",
        name="bank_status",
        verbose_name="وضعیت بانک",
        help_text="وضعیت بانک",
    )

    tracking_code=models.CharField(
        max_length=150,
        db_index=True,
        null=True,
        blank=True,
        db_column="tracking_code",
        db_comment="tracking_code",
        name="tracking_code",
        verbose_name="tracking_code",
        help_text="tracking_code",
    )


    amount=models.FloatField(
        verbose_name="مقدار",
        help_text="مقدار",
        db_index=True,
        null=True,
        blank=True,
    )


    user=models.ForeignKey(
        to=User,
        to_field="id",
        blank=True,
        null=True,
        db_index=True,
        db_column="user",
        verbose_name="کاربر",
        help_text="کاربر",
        on_delete=models.CASCADE,
    )


    created=models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="زمان ساخت",
        help_text="زمان ساخت",
        db_column="created",
        db_comment='created time',
        blank=True,
        null=True,
    )

    updated=models.DateTimeField(
        auto_now=True,
        db_index=True,
        help_text="زمان اخرین تغییر ",
        verbose_name="زمان اخرین تغییر",
        blank=True,
        null=True,

    )



    def __str__(self) -> str:
        return str(self.bank_name)
    


    class Meta:

        verbose_name="پرداخت ها"
        verbose_name_plural="پرداخت ها"


class Order(models.Model):

    id=models.UUIDField(
        default=uuid.uuid4,
        db_index=True,
        editable=False,

        unique=True,
        db_column="id",
        db_comment="id",
        primary_key=True
    )

    send_status=models.CharField(
        choices=SEND_STATUS,
        max_length=40,
        default="درانتظار یافتن اولین پیک",
        db_index=True,
        null=True,
        blank=True,
        verbose_name="وضیعت تحویل",
        help_text="وضیعت تحویل",
    )

    authority=models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True,
        db_column="authority",
        db_comment="Authority",
        verbose_name="Authority",
        help_text="Authority",
    )
    
    name=models.CharField(
        max_length=150,
        db_index=True,
        null=True,
        blank=True,
        verbose_name="name"

    )

    last_name=models.CharField(
        max_length=150,
        db_index=True,
        null=True,
        blank=True,
        verbose_name="last_name"
    )

    ORDER_STATUS=(
        ('PAID',"paid"),
        ('NOTPAID',"notpaid"),
    )

    order_status=models.CharField(
        max_length=110,
        verbose_name="order status",
        help_text="order status",
        db_index=True,
        db_column="order_status",
        choices=ORDER_STATUS,
        default="NOTPAID"
    )

    user=models.ForeignKey(
        to=User,
        verbose_name="user",
        help_text="user",
        db_index=True,
        on_delete=models.CASCADE,
        null=True,
        blank=True

    )

    payment=models.ForeignKey(
        to=Payment,
        verbose_name="payment",
        help_text="payment",
        db_index=True,
        on_delete=models.CASCADE,
        null=True,
        blank=True

    )

    items=models.ManyToManyField(
        to=CartItem,
        db_index=True,
        verbose_name="cart item",
        help_text="cart item"
    )

    custom_order_id=models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
        db_column="custom_order_id"
    )

    amount=models.FloatField(
        db_index=True,
        blank=True,
        null=True
    )

    final_amount=models.FloatField(
        db_index=True,
        blank=True,
        null=True,
    )

    used_copon=models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="used copon",
        help_text="used copon"
    )


    city=models.CharField(
        db_index=True,
        max_length=120,
        blank=True,
        null=True,
        verbose_name="city",
        help_text="city"
    )

    address=models.TextField(
        max_length=450,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="address",
        help_text="address",

    )

    zipcode=models.CharField(
        max_length=40,
        db_index=True,
        null=True,
        blank=True,
        verbose_name="zipcode",
        help_text="zipcode",

    )

    phone=models.CharField(
        max_length=40,
        db_index=True,
        null=True,
        blank=True,
        verbose_name="phone",
        help_text="phone",
    )

    email=models.EmailField(
        max_length=140,
        db_index=True,
        null=True,
        blank=True,
        verbose_name="email",
        help_text="email",
    )


    is_paid=models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='is paid',
        help_text="is paid"
    )



    created=models.DateTimeField(
                                    auto_now_add = True ,
                                    help_text = "created",
                                    verbose_name = "created",
                                    db_index = True,
                                    null=True,
                                        blank=True
                                )
    
    updated = models.DateTimeField( 
                                    auto_now = True ,
                                    help_text = "updated",
                                    verbose_name = "updated",
                                    db_index = True,
                                    null=True,
                                        blank=True

                                  )




    def __str__(self) -> str:
        return str(self.amount)+str(self.user)
    
    @property
    def created_irani(self):
        return datetime2jalali(self.created)
    
    @property
    def updated_irani(self):
        return datetime2jalali(self.updated)
    

    def save(self,*args,**kwargs):

        self.custom_order_id=generate_auto_custom_id()


        return super().save(*args,**kwargs)
    





class Copon(models.Model):

    expire=models.DateTimeField(
        db_index=True,
        blank=True,
        null=True,
        verbose_name="expire time",
        help_text="expire time",
    )

    copon_code=models.CharField(
        max_length=15,
        db_column="copon_code",
        db_index=True,
        verbose_name="copon code",
        help_text="cpon code"
    )

    is_active=models.BooleanField(
        db_index=True,
        blank=True,
        null=True,
        verbose_name="is active",
        help_text="is active"
    )

    percent=models.PositiveIntegerField(
        db_index=True,
        blank=True,
        null=True,
        verbose_name="percent",
        help_text="percent"
    )

    number_code=models.PositiveIntegerField(
        db_column="number_code",
        db_index=True,
        verbose_name='number code',
        help_text="number code",
        default=10
    )

    def __str__(self):
        return str(self.copon_code)
    

    class Meta:
        verbose_name="copon"
        verbose_name_plural="copon"


