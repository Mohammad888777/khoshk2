from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.core.exceptions import ValidationError
from .manager import UserManger,CodeManger

from jalali_date import datetime2jalali




def validate_phone(value:str):



    if type(value)!=str:
        raise ValidationError("phone type should be string")
    
    if len(value)!=11:
        raise ValidationError("phone length should be 11")
    
    if not value.isdigit():
        raise ValidationError("phone should be only digits")
    
    if not value.startswith("0"):
        raise ValidationError("phone should starts with 0")
    
    
    return value
    

class User(AbstractBaseUser,PermissionsMixin):

    username=models.CharField(
        max_length=150,
        db_index=True,
        db_column="username",
        blank=True,
        null=True,
        name="username",
        verbose_name="username",
        help_text="username",

    )

    phone=models.CharField(
        max_length=11,
        db_index=True,
        db_column="phone",
        db_comment="phone unique",
        name="phone",
        unique=True,
        blank=False,
        null=False,
        verbose_name="phone",
        help_text="phone",
        validators=[validate_phone]
    )

    first_name=models.CharField(
        max_length=100,
        db_index=True,
        db_column="first_name",
        db_comment="first name",
        blank=True,
        null=True,
        name="first_name",
        verbose_name="first name",
        help_text="first name",
        
    )


    last_name=models.CharField(
        max_length=100,
        db_index=True,
        db_column="last_name",
        db_comment="last name",
        blank=True,
        null=True,
        name="last_name",
        verbose_name="last name",
        help_text="last name",
        
    )


    email=models.EmailField(
        max_length=250,
        db_index=True,
        db_column="email",
        db_comment="email address",
        blank=True,
        null=True,
        unique=True,
        name="email",
        verbose_name="email",
        help_text="email",
    )

    is_admin=models.BooleanField(
        default=False,
        db_index=True,
        db_column="is_admin",
        db_comment="is_admin",
        name="is_admin",
        verbose_name="is user admin?",
        help_text="is user admin?",
    )

    
    is_staff=models.BooleanField(
        default=False,
        db_index=True,
        verbose_name="is user staff?",
        help_text="is user staff?",
    )



    is_active = models.BooleanField(
        default=False,
        db_index=True,
        db_column="is_active",
        db_comment="is_active",
        name="is_active",
        verbose_name="is user active?",
        help_text="is user active?"
    )

    

    is_superuser = models.BooleanField(
        default=False,
        db_index=True,
        db_column="is_superuser",
        db_comment="is_superuser",
        name="is_superuser",
        verbose_name="is user superuser?",
        help_text="is user superuser?",
    )


    date_joined = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        db_column="date_joined",
        db_comment="date_joined",
        name="date_joined",
        verbose_name="date joined",
        help_text="date joined"
    )

    user_ip=models.GenericIPAddressField(
        db_index=True,
        db_column="user_ip",
        db_comment='user_ip',
        name="user_ip",
        blank=True,
        null=True,
        verbose_name="user ip address",
        help_text="user ip address",
    )


    created = models.DateTimeField(
        auto_now_add=True,
        help_text="created time",
        verbose_name="created time",
        db_index=True,

    )

    updated = models.DateTimeField(
        auto_now=True,
        help_text="updated time",
        verbose_name="updated time",
        db_index=True,

    )

    USERNAME_FIELD="phone"

    REQUIRED_FIELDS=[
        'username',
        "email",
   
    ]

    objects=UserManger()

    @property
    def created_irani(self):
        return datetime2jalali(self.created)

    def __str__(self):
        return str(self.phone)
    
    def has_perm(self, perm, obj = ...):
        return self.is_admin and self.is_active and self.is_superuser
    
    def has_module_perms(self, app_label):
        return True




    class Meta:
        verbose_name="user" 
        verbose_name_plural="user"
        ordering=[
            "created"
        ]

        get_latest_by=["created"]
        base_manager_name="objects"









class Code(models.Model):


    user=models.OneToOneField(
        to=User,
        to_field='id',
        db_index=True,
        blank=False,
        null=False,

        on_delete=models.CASCADE,
        verbose_name="user",
        help_text="user"
    )


    exp=models.DateTimeField(

        db_index=True,
        blank=True,
        null=True,
        name="exp",
        verbose_name="expire time",
        help_text="expire time",

    )

    token=models.CharField(
        max_length=7,
        unique=True,
        db_index=True,
        help_text="otp code",
        verbose_name="code to verify"
    )
    @property
    def created_irani(self):
        return datetime2jalali(self.created)

    def __str__(self) -> str:
        return str(self.token)
    
    objects=CodeManger()
    
    

    class Meta:

        verbose_name="otp code"
        verbose_name_plural="otp code"

    



