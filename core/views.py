from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.db.models import Q,F
from .models import FirstSlider,Product,Comment
from card.models import CartItem












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
