from django.contrib import admin

from .models import Copon,Payment,Order



admin.site.register([
    Copon,
    Payment,
    Order
])
