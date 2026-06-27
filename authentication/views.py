from typing import Any
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render#render/redirect
from django.views import View
from django.views.generic import FormView,RedirectView
from authentication.forms import Loginform
from django.contrib.auth import authenticate
from django.contrib import auth
from django.forms.utils import ErrorDict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

#如果清理cookie显示403  -->  Forbidden (CSRF cookie not set.): /authentication/user/login/
# @method_decorator(csrf_exempt,name='dispatch')

class LoginView(FormView):
    template_name='authentication/user_login.html'
    form_class=Loginform

    def get_context_data(self, **kwargs):
        context=super().get_context_data()
        context['active_page']='login'
        return context
    
    def form_valid(self, form):#表单判断成功后
        user=form.authenticate_user()      
        #print(f"errors={type(form.errors)}")
        if not user:
            state='error'
            msg='用户名或密码错误'
            return JsonResponse({'state':state,'msg':msg})
        else:
            state='success'
            auth.login(self.request,user=user)
            #print(self.request.user)
            return JsonResponse({'state':state})
    
""" class LogoutView(RedirectView):
    pattern_name='homepage'
    
    def get_redirect_url(self, *args, **kwargs) -> str | None:
        auth.logout(self.request)
        return super().get_redirect_url() """
    
class LogoutView(View):

    def get(self,request):
        auth.logout(request)
        print(request.user)
        return redirect('homepage')
    
    