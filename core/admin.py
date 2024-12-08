from django.contrib import admin
from .models import FirstSlider,Product,Comment,ContactUs


admin.site.register(
    [
        FirstSlider,Product,Comment,ContactUs
    ]
)