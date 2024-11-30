from django.contrib import admin
from .models import FirstSlider,Product,Comment


admin.site.register(
    [
        FirstSlider,Product,Comment
    ]
)