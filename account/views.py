from django.shortcuts import render,get_object_or_404,redirect
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from .models import User,Code,validate_phone
from datetime import datetime,timezone,timedelta
from .utils import createOtpToken,send_otp
from django.contrib.auth import login,authenticate,logout
from .mixins import NotLogin,ControlThrottle,ControlThrottleForResend





class LoginView(
                 NotLogin
                # ,ControlThrottle
                ,View
                ):

    def get(self,request,*args,**kwargs):

        return render(request,"account/login.html")
    

    def post(self,request,*args,**kwargs):

        with transaction.atomic():

            data:dict=request.POST

            if not data.get("phone"):

                return JsonResponse({
                    "phone":True,
                    "error":True
                })
            

            try:
                validate_phone(data.get('phone'))
            except Exception as e:
                return JsonResponse({
                    "error":True,
                    "phone":True
                })
            
            phone=data.get("phone")
            
            try:
                user=User.objects.get(phone=phone)
            
            except User.DoesNotExist:
                user=User.objects.create_user(
                    phone=phone
                )


            
            c=Code.objects.filter(
                user=user
            ).delete()

            now=datetime.now(timezone.utc)+timedelta(minutes=5)

            new_otp=createOtpToken()

            new_code=Code.objects.create(
                exp=now,
                token=new_otp,
                user=user
            )

            send_otp(str(user.phone),str(new_code.token))

            self.request.session["phone"]=str(user.phone)
            self.request.session["code"]=str(new_code.token)

            return JsonResponse({
                "otp_send":True,
            })








class VerifyView(
        NotLogin,
        # ControlThrottle,
        View
    ):


    def get(self,request,*args,**kwargs):
        
        return render(request,"account/verify.html")


    def post(self,request,*args,**kwargs):

        with transaction.atomic():

            data=request.POST

            if not data.get("otp"):
                return JsonResponse({
                    "error":True,
                    "otp":True
                })
            
            

            user_phone=self.request.session.get("phone")
            now=datetime.now(timezone.utc)
            
            try:
                o=Code.objects.get(
                                        token=data.get("otp"),
                                        user__phone=user_phone,
                                        exp__gte=now
                                   )
            except Code.DoesNotExist:
                return JsonResponse({
                    "error":True,
                    "otp_not_ex":True
                })
            
            user=get_object_or_404(User,phone=user_phone,is_active=True)
            auth=authenticate(
                username=user.phone,
                password=str(user.id)
            )

            if auth is not None:

                login(request,user)

                return JsonResponse({
                    "login":True
                })
            
            else:

                return JsonResponse({
                    "error":True,
                    "login_problem":True
                })
            



            


class ResendOtp(
        NotLogin,
        ControlThrottleForResend,
        View
):
    
    def post(self,request,*args,**kwargs):

        with transaction.atomic():

            user_phone=self.request.session.get("phone")

            if not user_phone:

                return JsonResponse({
                    "error":True,
                    "user_phone_session":True
                })
            user=None

            try:
                user=User.objects.get(
                    is_active=True,
                    phone=user_phone
                )
            

            except User.DoesNotExist:
                user=None

            if not user:

                return JsonResponse({
                    "error":True,
                    "user_ex":True
                })
            
            c=Code.objects.filter(
                user=user,
            ).delete()

            now=datetime.now(timezone.utc)+timedelta(minutes=5)

            new_otp=createOtpToken()

            new_code=Code.objects.create(
                exp=now,
                token=new_otp,
                user=user
            )


            send_otp(str(user.phone),str(new_code.token))

            self.request.session["phone"]=str(user.phone)
            self.request.session["code"]=str(new_code.token)


            return JsonResponse({
                "otp_send":True,
            })
        