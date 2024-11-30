from django.http import JsonResponse
from django.shortcuts import redirect


class LoginRequired():

    def dispatch(self,request,*args,**kwargs):

        if not  request.user.is_authenticated:

            if request.is_ajax():
                
                return JsonResponse({
                "error":True,
                "loggin_required":True
            })

            else:

                return redirect("home")
            

        
        return super().dispatch(request,*args,**kwargs)
