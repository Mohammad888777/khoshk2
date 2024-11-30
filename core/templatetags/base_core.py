from django.template import Library
from card.models import CartItem


register=Library()



@register.simple_tag(takes_context=True)
def test_in_cart(context,product_id):

    user=context["request"].user

    return CartItem.objects.filter(
        user=user,
        cart_status="notPaid",
        product_id=product_id
    )




