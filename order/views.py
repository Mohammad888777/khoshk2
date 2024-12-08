from django.shortcuts import render,redirect,get_object_or_404
from django.db import transaction
from account.models import User
from django.views import View
from django.http import JsonResponse

from card.mixins import LoginRequired
from account.mixins import NotLogin,ControlThrottle
from .models import Copon,Order,Payment
from card.models import Cart,CartItem
from datetime import timezone,timedelta,datetime
from account.utils import convert_str_to_uuid
from django.db.models import Q,F

import requests
import json






MMERCHANT_ID = '8c00df17-3d8e-4b97-8ff7-dee5e02e945f'  # Required
ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
# amount = 100000  # Amount will be based on Toman  Required
description = u'توضیحات تراکنش تستی'  # Required
email = 'user@userurl.ir'  # Optional
mobile = '09123456789'  # Optional
ZP_API_REQUEST = f"https://sandbox.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = f"https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = f"https://sandbox.zarinpal.com/pg/StartPay/"




class CheckoutView(
    View,
    LoginRequired,
):
    
    def get(self,request,*args,**kwargs):

        user=request.user
        o_id=self.kwargs.get("id")
        order=get_object_or_404(Order,id=o_id,
                                user=user,
                                order_status="NOTPAID",
                                is_paid=False,
                                send_status="درانتظار یافتن اولین پیک",
                                # used_copon=False
                                )
        


        context={
            "order":order
        }

        return render(request,"order/checkout.html",context)
    
    



class AddCopon(
    View,
    LoginRequired,
    ControlThrottle,
):
    

    def post(self,request,*args,**kwargs):

        with transaction.atomic():

            data:dict=request.POST
            user=request.user

            c=data.get('copon')
            o=data.get("order")

            if not c:

                return JsonResponse({
                    "copon":True,
                    "error":True
                })
            
            if not o:

                return JsonResponse({
                    "order":True,
                    "error":True
                })
            
            
            co=None

            now=datetime.now(tz=timezone.utc)

            try:
                co=Copon.objects.get(
                    copon_code=c,
                    is_active=True,
                    expire__gte=now,
                    # number_code__gt=0
                )
            except Copon.DoesNotExist:
                co=None
            

            if not co:

                return JsonResponse({
                    "copon_ex":True,
                    "error":True
                })
            
            
            order=None

            try:

                order=Order.objects.get(
                    user=user,
                    is_paid=False,
                    id=convert_str_to_uuid(o),
                    order_status="NOTPAID",
                    payment__isnull=True,
                    used_copon=False
                )
            
            except Order.DoesNotExist:
                order=None
            
            if not order:

                return JsonResponse({
                    "error":True,
                    "order_ex":True
                })
            


            order.final_amount=order.final_amount-((order.final_amount*co.percent)/100)
            order.used_copon=True
            order.save()
            co.number_code-=1
            co.save()

            CallbackURL = f'http://127.0.0.1:8000/order/afterPay/{order.id}/'
    

            
            data = {    
                    "merchant_id": MMERCHANT_ID,
                    "amount":int(order.final_amount),
                    "description":"asd",
                    "metadata": {
                        "mobile": "09308880854",
                        "email": "info.test@gmail.com"
                    },
                    "callback_url": CallbackURL,
                }

            data = json.dumps(data)

            headers = {'content-type': 'application/json', 'content-length': str(len(data)) }

            try:

                response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

                if response.status_code == 200:
                    response = response.json()
                    if response.get("data").get("code") == 100:

                        order.authority=str(response.get("data").get("authority"))
                        order.save()

                        return JsonResponse({
                            "new_amount":True,
                        })


            except Exception as  e:

                return JsonResponse({
                    "error":True,
                    "pay":True
                })

            





class AddOrderView(
      View,
    LoginRequired,
    # ControlThrottle,
):
    
    def post(self,request,*args,**kwargs):

        with transaction.atomic():

            user=request.user

            c=CartItem.objects.filter(
                user=user,
                cart_status="notPaid",
            )


            o=Order.objects.filter( 
                items__in=c,
                is_paid=False
            )
            o.delete()

            stat=CartItem.objects.cart_static(user=user)

            new_order=Order.objects.create(
                user=user,
                amount=stat.get("total_without_tax"),
                final_amount=stat.get("total_without_tax"),
            )

            for i in c:
                new_order.items.add(i)
                new_order.save()
            new_order.save()


            CallbackURL = f'http://127.0.0.1:8000/order/afterPay/{new_order.id}/'
    

            
            data = {    
                    "merchant_id": MMERCHANT_ID,
                    "amount":int(new_order.final_amount),
                    "description":"asd",
                    "metadata": {
                        "mobile": "09308880854",
                        "email": "info.test@gmail.com"
                    },
                    "callback_url": CallbackURL,
                }

            data = json.dumps(data)

            headers = {'content-type': 'application/json', 'content-length': str(len(data)) }

            try:

                response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)

                if response.status_code == 200:
                    response = response.json()
                    if response.get("data").get("code") == 100:

                        new_order.authority=str(response.get("data").get("authority"))
                        new_order.save()

                        return JsonResponse({
                            "saved":True,
                            'url': ZP_API_STARTPAY + str(response.get("data").get("authority")),
                            "id":new_order.id
                        }) 


            except Exception as  e:

                return JsonResponse({
                    "error":True,
                    "pay":True
                })
            




class AfterPay(LoginRequired,View):

    def get(self,request,*args,**kwargs):

        o=get_object_or_404(Order,
                            id=self.kwargs.get("id"),
                            user=request.user,
                            order_status="NOTPAID",
                            is_paid=False,

                            )

        data = {
                "merchant_id": MMERCHANT_ID,
                "amount": int(o.final_amount),
                "authority": str(o.authority),
            }


        data = json.dumps(data)

        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)
        confimred=False
        try:

            res=response.json()

            print(res)
            
            if res.get("data").get("code")==101 \
                or res.get("data").get("message")=="Verified" \
                or res.get("data").get("message")=="Paid":
                
                p=Payment.objects.create(
                    card_hash=res.get("data").get("card_hash"),
                    card_pan=res.get("data").get("card_pan"),
                    ref_id=res.get("data").get("ref_id"),
                    bank_status=res.get("data").get("code"),
                    amount=o.final_amount,
                    user=o.user,
                )


                o.is_paid=True
                o.order_status="PAID"
                o.payment=p
                o.save()

                for i in o.items.all():
                    i.cart_status="paid"

                    i.save()
                o.save()

                confimred=True



        except Exception as e:

            confimred=False
        
        return render(request,"order/afterPay.html",
                      context={
                          'confimred':confimred
                      })
                    






class PaymentView(
    LoginRequired,
    View
):
    
    def get(self,request,*args,**kwargs):

        user=request.user

        name=self.request.GET.get("name")
        city=self.request.GET.get("city")
        address=self.request.GET.get("address")

        o=get_object_or_404(Order,
                            id=self.kwargs.get("id"),
                            user=request.user,
                            order_status="NOTPAID",
                            is_paid=False,
        )

        o.name=name
        o.city=city
        o.address=address
        o.save()

        return JsonResponse({
            "link":ZP_API_STARTPAY+o.authority
        })





class MyOrdersView(LoginRequired,View):

    def get(self,request,*args,**kwargs):

        user=request.user
        o=Order.objects.filter(
            user=user
        )

        context={
            'orders':o,
            'user':user
        }


        return render(request,"order/myorders.html",context)
