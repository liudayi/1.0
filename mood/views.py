from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from utils.mixins import AjaxResponseMixin,AtomicMixin
from .models import Mood
from .mixin import MoodMixin
# Create your views here.
class MoodListView(LoginRequiredMixin,ListView):
    login_url='user-login'
    model=Mood
    fields=['title','mood_type','create_time','content','image','mood_type']

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['mood_list']=Mood.objects.all()
        return context

class MoodCreateView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,CreateView):
    login_url='user-login'
    model=Mood
    fields=['title','content','image','mood_type']
    template_name='mood/mood_create_form.html'
    success_url=reverse_lazy('mood-list')

    def get_template_names(self) -> list[str]:
        user_agent=self.request.META.get("HTTP_USER_AGENT","").lower()
        keyword=['mobile','iphone','ipad','android']
        if any(key in user_agent for key in keyword):
            return ["mood/mood_create_form_mobile.html",self.template_name]
        else:
            return self.template_name
        
    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("失败原因"+form.errors.as_json())
        return super().form_invalid(form)    
    
class MoodUpdateView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,UpdateView):
    login_url='user-login'
    model=Mood
    fields=['title','mood_type','content','image']
    template_name_suffix='_update_form'
    success_url=reverse_lazy('mood-list')

    def form_valid(self, form):
        return super().form_valid(form)
    
class MoodDeleteView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,DeleteView):
    login_url='user-login'
    model=Mood
    success_url=reverse_lazy('mood-list')

    def delete(self, request, *args, **kwargs):
        obj=self.get_object()
        print(obj.image)
        if obj.image:           
            obj.image.delete(save=False)
        return super().delete(request, *args, **kwargs)

    def post(self,request,*args,**kwargs):
        obj=self.get_object()
        print(obj.image)
        if obj.image:           
            obj.image.delete(save=False)
        return super().post(request,*args,**kwargs)

class MoodTimeLineView(MoodMixin,LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,ListView):
    login_url='user-login'
    model=Mood
    fields=['title','content','mood_type','image']
    context_object_name='mood_list'
    template_name='mood/mood_time_line.html'
    paginate_by=10
    
