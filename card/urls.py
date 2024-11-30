from django.urls import path
from . import views

urlpatterns=[

    path("mycart/",views.MyCartView.as_view(),name="mycart"),
    path("add/<int:id>/",views.AddCart.as_view(),name="add"),

]