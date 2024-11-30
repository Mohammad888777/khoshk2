from django.db.models import Manager
from django.db.models import Sum,F


class CartItemManager(Manager):

    def cart_static(self,user):

        return self.filter(
                user=user,cart_status="notPaid",
            ).annotate(
                each_costs=
                    F('quantity')*F("product__price")
            ).aggregate(
                q=Sum("quantity"),
                total_without_tax=Sum("each_costs"),
                # tax=(Sum("each_costs")*10)/100,
                # final_total=Sum("each_costs")+(Sum("each_costs")*10)/100

            )
    