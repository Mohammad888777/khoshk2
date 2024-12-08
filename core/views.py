from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.db.models import Q,F
from .models import FirstSlider,Product,Comment,ContactUs
from django.http import JsonResponse
from django.db import transaction












def home(request):
    

    slider=FirstSlider.objects.filter(
        is_active=True,
        
    )

    products=Product.objects.filter(
        is_active=True
    )

    comments=Comment.objects.filter(
        is_active=True
    )

        


    context={
        'slider':slider,
        "products":products,
        'comments':comments
    }


    return render(request,"main/home.html",context)



def productDetail(request,id):

    p=get_object_or_404(Product,is_active=True,id=id)

    related=Product.objects.filter(
        is_active=True
    ).exclude(
        id=p.id
    )

    context={
        'p':p,
        'related':related
    }

    return render(request,"main/detail.html",context)







def shopView(request,*args,**kwargs):

    p=Product.objects.filter(
        is_active=True
    )

    context={
        'products':p
    }


    return render(request,"main/shop.html",context)




def aboutUs(request):

    return render(request,"main/about.html")




def contact(request):

    if request.method=="POST":

        with transaction.atomic():

            data:dict=request.POST

            name=data.get("name",None)
            phone=data.get("phone",None)
            text=data.get("text",None)

            if not name:return JsonResponse({"name":True,"error":True})
            if not phone:return JsonResponse({"phone":True,"error":True})
            if not text:return JsonResponse({"text":True,"error":True})

            new_con=ContactUs.objects.create(
                name=name,
                phone=phone,
                text=text
            )

            return JsonResponse({
                "saved":True
            })
        

    return render(request,"main/contact.html")
