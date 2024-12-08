from django.urls import path,include
from . import views

urlpatterns=[
    path("",views.home,name="home"),
    path("about/",views.aboutUs,name="about"),
    path("shop/",views.shopView,name="shop"),
    path("contact/",views.contact,name="contact"),
    path("<int:id>/",views.productDetail,name="detail"),
]