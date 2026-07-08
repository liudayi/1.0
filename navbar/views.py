from typing import Any
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from navbar.models import NavbarItem
from django.contrib.auth.decorators import *
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixins import AjaxResponseMixin,AtomicMixin
import json
# Create your views here.
class NavbarListView(LoginRequiredMixin,ListView):
    """
    展示导航项,有一个列表页
    """
    login_url='user-login'
    model=NavbarItem#框架会根据model自动执行model.objects.all()
    template_name='navbar/navitem_list.html'#根据template_name渲染页面,填入数据
    fields=['title','url','order']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['navbar_list']=NavbarItem.objects.all()
        return context


class NavCreateView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,CreateView):
    """
    1.要设置权限,仅登录用户可添加新导航页
    //加上了装饰器
    //不能用login_required,类有自己的装饰器
    2.检查数据是否合法,不合法应返回错误信息//框架应该会自己检查
    3.前端代码展示顺序是自己手动加的,后面要改代码
    """
    login_url='user-login'
    model=NavbarItem
    template_name='navbar/navitem_create_form.html'
    fields=['title','url','order']
    success_url=reverse_lazy('navbar-list')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """
        判断并修改当展示顺序冲突的情况
        不应该自己修改而是输出提示给用户
        首先是判断有没有冲突
        """
        if NavbarItem.objects.filter(order=form.cleaned_data.get('order')).exists():
            return JsonResponse({'state':'error'})
       
        return super().form_valid(form)


class NavUpdateView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,UpdateView):
    login_url='user-login'
    model=NavbarItem
    success_url=reverse_lazy('navbar-list')
    fields=['title','url','order']
    template_name='navbar/navitem_update_form.html'
    context_object_name='navitem'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        """
        判断并修改当展示顺序冲突的情况
        """
        obj=self.get_object()
        new_order=form.cleaned_data.get('order')
        old_order=obj.order
        if NavbarItem.objects.filter(order=new_order).exists() and old_order!= new_order:
            if old_order<new_order:
                NavbarItem.objects.filter(order__gte=old_order,order__lte=new_order).update(order=F('order')-1)
            else:
                NavbarItem.objects.filter(order__lte=old_order,order__gte=new_order).update(order=F('order')+1)
            obj.order=new_order
            msg=f'已把{old_order}修改为{new_order}'
        else:
            msg=f"无需调整"
        
        response=super().form_valid(form)#调用父类函数,执行数据库保存

        if isinstance(response,JsonResponse):
            data=json.loads(response.content.decode('utf-8'))
            data['state']='success'
            data['msg']=msg
            return JsonResponse(data)
        
        return response
            


    
class NavDeteleView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,DeleteView):
    """
    当删除其中一个导航项时,该导航项后面的导航项的展示顺序要一次递进
    建议写在model里
    """
    login_url='user-login'
    model=NavbarItem
    #template_name='navbar/navitem_list.html'
    def post(self, request: HttpRequest, *args: str, **kwargs: Any):
        obj=self.get_object()
        NavbarItem.objects.filter(order__gt=obj.order).update(order=F('order')-1)
        obj.delete()
        return JsonResponse({'state':'success'})
