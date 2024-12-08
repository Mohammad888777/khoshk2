from django.urls import path
from . import views

urlpatterns=[

    path("mycart/",views.MyCartView.as_view(),name="mycart"),
    path("add/<int:id>/",views.AddCart.as_view(),name="add"),
    path("plus/<int:id>/",views.IncreaseNumber.as_view(),name="plus"),
    path("min/<int:id>/",views.DecreaseNumber.as_view(),name="neg"),
    path("remove/<int:id>/",views.RemoveItem.as_view(),name="remove"),

]