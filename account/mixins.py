from django.http import JsonResponse
from django.shortcuts import redirect
from throttle.decorators import throttle
from django.utils.decorators import method_decorator


class NotLogin():

    def dispatch(self,request,*args,**kwargs):

        if request.user.is_authenticated:
            if request.is_ajax():
                

                return JsonResponse({
                "error":True,
                "already_logged_in":True
            })
            else:

                return redirect("home")

        
        return super().dispatch(request,*args,**kwargs)



class ControlThrottle():

    @method_decorator(throttle(zone="default"))
    def dispatch(self,request,*args,**kwargs):

        return super().dispatch(request,*args,**kwargs)
    
    


class ControlThrottleForResend():

    @method_decorator(throttle(zone="resend"))
    def dispatch(self,request,*args,**kwargs):

        return super().dispatch(request,*args,**kwargs)
    