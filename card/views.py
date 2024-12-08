from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from .models import Cart,CartItem
from account.models import User
from django.views import View
from account.mixins import NotLogin,ControlThrottle
from django.db import transaction
from core.models import Product
from .mixins import LoginRequired




class AddCart(
            LoginRequired,
            ControlThrottle,
            View
              ):
    
    def post(self,request,*args,**kwargs):

        with transaction.atomic():

            user=request.user
            p=None

            try:
                p=Product.objects.get(
                    is_active=True,
                    id=self.kwargs.get("id")
                )

            except Product.DoesNotExist:
                p=None
            
            if not p:

                return JsonResponse({
                    "product":True,
                    "error":True
                })
        
            
            c=None

            try:
                c=CartItem.objects.get(
                    user=user,
                    cart_status="notPaid",
                    product=p
                )
            except CartItem.DoesNotExist:
                c=None

            if c:
                c.quantity+=1
                c.save()
            else:
                
                c=CartItem.objects.create(
                    user=user,
                    product=p,
                    quantity=1,
                )
            

            static=CartItem.objects.cart_static(user=user)

            return JsonResponse({
                "added":True,
                "static":static
            })
        








class MyCartView(
    LoginRequired,
    # ControlThrottle,
    View
):
    


    def get(self,request,*args,**kwargs):

        user=request.user

        c_item=CartItem.objects.filter(
            user=user,
            cart_status="notPaid"
        )

        stat=CartItem.objects.cart_static(user=user)

        context={
            "items":c_item,
            "stat":stat
        }   

        return render(request,"cart/myCart.html",context)








class ChangeItemQuantity(
    LoginRequired,
    ControlThrottle,
    View
    ):

    def post(self,request,*args,**kwargs):

        with transaction.atomic():

            data:dict=self.request.POST


            if not "quantity" in data:

                return JsonResponse({
                    "error":True,
                    "quantity":True
                })

            c_item=get_object_or_404(
                CartItem,
                id=self.kwargs.get("id"),
                user=request.user
            )

            if int(data.get("quantity"))==0:

                c_item.delete()
                
                return JsonResponse({
                    "deleted":True
                })
            
            else:

                c_item.quantity=int(data.get('quantity'))

            c_item.save()

            return JsonResponse({
                "response":c_item.quantity,
            })
    







class IncreaseNumber(
    LoginRequired,
    ControlThrottle,
    View
    ):


    def post(self,request,*args,**kwargs):

        with transaction.atomic():

            data:dict=self.request.POST

            c=get_object_or_404(
                    CartItem,
                    id=self.kwargs.get("id"),
                    user=request.user,
                    cart_status="notPaid"
                )   
            c.quantity+=1
            c.save()


            return JsonResponse({
                "saved":True
            })
    


class DecreaseNumber(
    LoginRequired,
    ControlThrottle,
    View
):
    

    def post(self,request,*args,**kwargs):

        with transaction.atomic():

            c=get_object_or_404(
                    CartItem,
                    id=self.kwargs.get("id"),
                    user=request.user,
                    cart_status="notPaid"
                )   
            
            if c.quantity>0:
                if c.quantity==1:
                    c.delete()

                    return JsonResponse({
                        "saved":True
                    })

                else:

                    c.quantity-=1
                    c.save()
    
            return JsonResponse({
                "saved":True
            })
        

class RemoveItem (LoginRequired,
    ControlThrottle,
    View
):
    

    def post(self,request,*args,**kwargs):

        with transaction.atomic():

            c=get_object_or_404(
                    CartItem,
                    id=self.kwargs.get("id"),
                    user=request.user,
                    cart_status="notPaid"
                )   
            c.delete()
    
            return JsonResponse({
                "deleted":True
            })





