from django.db import models
from django.core.validators import FileExtensionValidator
from account.models import User


class FirstSlider(models.Model):

    image=models.ImageField(
        db_index=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "png","jpg","jpeg"
                ]
            )
        ],

    )


    # test=models.TextField(
    #     null=True,
    #     blank=True
    # )

    link_to_go=models.URLField(
        db_index=True,
        blank=True,
        null=True,
        verbose_name="link",
        help_text="link",

    )

    is_active=models.BooleanField(
        default=True,
        verbose_name="is_active",
        help_text="is_active",
        db_index=True
    )

    title=models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="title",
        help_text="title",

    )

    description=models.TextField(
        db_index=True,
        verbose_name="description",
        help_text="description",
    )

  


    def __str__(self):
        return str(self.title)
    


    class Meta:

        verbose_name="slider"
        verbose_name_plural="slider"








class Product(models.Model):


    is_active=models.BooleanField(
        default=True,
        verbose_name="is_active",
        help_text="is_active",
        db_index=True
    )
    
    name=models.CharField(
        max_length=100,
        db_index=True,
        verbose_name="name",
        help_text="name",
    )

    image=models.ImageField(
        db_index=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "png","jpg","jpeg"
                ]
            )
        ],
        blank=True,
        null=True

    )

    description=models.TextField(
        blank=True,
        null=True,
        db_index=True,
        verbose_name="description",
        help_text="description",
        db_column="description"
    )

 
    price=models.PositiveIntegerField(
    
        db_index=True,
        verbose_name="price",
        help_text="price",
        blank=True,
        null=True
    )





    stock_number=models.PositiveIntegerField(
        db_index=True,
        verbose_name="stock kilogramm",
        help_text="stock kilogramm",
        blank=True,
        null=True
    )



    



    in_stock=models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="in stock",
        help_text="in stock",
        blank=True,
        null=True
    )


    created=models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="created time",
        help_text="created time"
    )

    updated=models.DateTimeField(
        auto_now=True,
        db_index=True,
        db_column="updated",
        name="updated",
        verbose_name="updated time",
        help_text="updated time"
    )


    def __str__(self):
        return str(self.name)+" " +str(self.price)
    




class Comment(models.Model):

    text=models.TextField(
        db_index=True
    )

    name=models.CharField(
        max_length=100,
        db_index=True,
        blank=True
    )

    city=models.CharField(
        max_length=150,
        db_index=True
    )

    is_active=models.BooleanField(
        default=True,
        blank=True,
        db_index=True
    )

    created=models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="created time",
        help_text="created time"
    )

    updated=models.DateTimeField(
        auto_now=True,
        db_index=True,
        db_column="updated",
        name="updated",
        verbose_name="updated time",
        help_text="updated time"
    )






class ContactUs(models.Model):


    name=models.CharField(
        max_length=150,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="name",
        help_text="name"
    )

    phone=models.CharField(
        max_length=150,
        db_index=True,
        blank=True,
        null=True,
        verbose_name="phone",
        help_text="phone"
    )

    text=models.TextField(
        db_index=True,
        blank=True,
        null=True
    )


    

    created=models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name="created time",
        help_text="created time"
    )

    updated=models.DateTimeField(
        auto_now=True,
        db_index=True,
        db_column="updated",
        name="updated",
        verbose_name="updated time",
        help_text="updated time"
    )