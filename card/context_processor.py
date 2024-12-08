from .models import CartItem
from django.db.models import Sum


def item_count(request):

    if request.user.is_authenticated:
        
        c=CartItem.objects.filter(
            cart_status="notPaid"
        ).aggregate(c=Sum("quantity"))

        if c.get('c'):
             
            return {"count":c.get("c")}
        
        else:

            return {
                "count":0
            }


    else:

        return {
            "count":0
        }