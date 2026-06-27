from typing import Any
from django.shortcuts import render
from django.views.generic import ListView,UpdateView,CreateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixins import AjaxResponseMixin,AtomicMixin
from .models import LinkItem
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.db.models import F
from django.urls import reverse_lazy
# Create your views here.
class LinkListView(LoginRequiredMixin,ListView):
    login_url='user-login'
    template_name='link/link_list.html'
    model=LinkItem
    fields=['title','url','description','order']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['link_list']=LinkItem.objects.all()
        return context
    
class LinkCreateView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,CreateView):
    login_url='user-login'
    model=LinkItem
    fields=['title','url','description','order']
    template_name='link/link_create_form.html'
    success_url=reverse_lazy('link-list')

    def form_valid(self, form):
        if LinkItem.objects.filter(order=form.instance.order).exists():
            return JsonResponse({'state':'error','msg':'该序号已存在'})
        else:
            return super().form_valid(form)
    
class LinkUpdateView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,UpdateView):

    login_url='user-login'
    model=LinkItem
    fields=['title','url','description','order']
    template_name='link/link_update_form.html'
    success_url=reverse_lazy('link-list')

    def form_valid(self, form):
        new_order=form.instance.order
        old_order=LinkItem.objects.get(pk=form.instance.pk).order
        print(new_order,old_order,LinkItem.objects.all())
        if new_order>old_order:
            LinkItem.objects.filter(order__gt=old_order,order__lte=new_order).update(order=F('order')-1)
        elif new_order<old_order:
            LinkItem.objects.filter(order__gte=new_order,order__lt=old_order).update(order=F('order')+1)
        print(LinkItem.objects.all().iterator())
        return super().form_valid(form)
    
class LinkDeleteView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,DeleteView):
    login_url='user-login'
    model=LinkItem
    fields=['title','url','description','order']
    success_url=reverse_lazy('link-list')

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        obj=self.get_object()
        LinkItem.objects.filter(order__gt=obj.order).update(order=F('order')-1)
        super().post(request,*args,**kwargs)
        return JsonResponse({'state':'success'})
    