from django.urls import path
from . import views



urlpatterns=[

    path("orders/",views.MyOrdersView.as_view(),name="myorders"),
    path("addcopon/",views.AddCopon.as_view(),name="copon"),
    path("addOrder/",views.AddOrderView.as_view(),name="addOrder"),
    path("checkout/<uuid:id>/",views.CheckoutView.as_view(),name="checkout"),
    path("afterPay/<uuid:id>/",views.AfterPay.as_view(),name="afterPay"),
    path("paymentView/<uuid:id>/",views.PaymentView.as_view(),name="paymentView"),


]