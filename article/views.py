from datetime import datetime
import os,posixpath
from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Category,Article,Purepage
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixins import AjaxResponseMixin,AtomicMixin
from django.views.generic import CreateView,ListView,UpdateView,DeleteView,DetailView,View
from django.urls import reverse_lazy
from uuid import uuid4
from config import settings
from django.core.files.storage import default_storage
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.db.models import Count
from utils.mixins import FrontMixin
# Create your views here.

#CHANGE:修改完成,删除了get_context_data()
class BlogListView(LoginRequiredMixin,ListView):
    #后台管理列表
    model=Article
    login_url=reverse_lazy('user-login')
    #context_object_name='essay_list'
    template_name='article/blog_list.html'#后台
    
    #DONE:限制用户只能查看自己的文章
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['essay_list']=Article.objects.filter(author=self.request.user)
        return context

class BlogCreateView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,CreateView):
    model=Article
    login_url=reverse_lazy('user-login')
    fields=['title','category','summary','content']#editor_id是富文本编辑器的意思
    success_url=reverse_lazy('blog-list-backend')
    #还要添加图片#额外写image_upload类适配
    template_name='article/blog_create_form.html'
    
    #DONE:绑定用户
    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any):
        context=super().get_context_data(**kwargs)
        context['category_list']=Category.objects.all()
        return context

class BlogUpdateView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,UpdateView):
    model=Article
    login_url=reverse_lazy('user-login')
    success_url=reverse_lazy('blog-list-backend')
    fields=['title','category','summary','content']
    template_name='article/blog_update_form.html'
    #context_object_name='blog'

    #TODO:限制用户只能修改自己的文章
    def get_object(self, queryset=None) -> Model:
        obj=super().get_object(queryset)
        if obj.author != self.request.user:
            raise Http404("不要尝试修改别人的文章")
        return obj
    
#DONE:前端代码没改
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['blog']=self.object
        context['category_list']=Category.objects.all()
        return context

class BlogDeleteView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,DeleteView):
    model=Article
    login_url=reverse_lazy('user-login')
    success_url='blog-list-backend'

#CHANGE:修改完成,删除了get_context_data(),把点击量增加的步骤写到了get_object()里
class ArticleDetailView(LoginRequiredMixin,FrontMixin,AjaxResponseMixin,DetailView):
    model=Article
    login_url=reverse_lazy('user-login')
    template_name='article/article_detail.html'
    context_object_name='article'

    def get_object(self, queryset = None) -> Model:
        #query_set=None是必须的,这是父类函数参数,重写时不能私下改变
        obj=super().get_object(queryset=queryset)
        obj.show_times+=1
        obj.save()
        return obj
        
#CHANGE:已删除ArticleListView,因为对应的article/article_list.html并没有在使用

class CategoryCreateView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,CreateView):
    login_url=reverse_lazy('user-login')
    model=Category
    template_name='article/category_create_form.html'
    success_url=reverse_lazy('category-list')
    fields="__all__"

class CategoryListView(LoginRequiredMixin,AjaxResponseMixin,ListView):
    model=Category
    login_url=reverse_lazy('user-login')
    context_object_name='category_list'
    template_name='article/category_list.html'

#CHANGE:修改完成
class CategoryWeightView(LoginRequiredMixin,FrontMixin,AjaxResponseMixin,ListView):
    #目录详情页.绑定homepage.
    model=Category
    login_url=reverse_lazy('user-login')
    template_name='website/frontend/homepage.html'
    context_object_name='article_list'
    paginate_by=5
    #因为article_weight.html也是搭载在homepage.html上的,所以要写article_list

    #TODO:后期可以加上category=None的情况。
    def get_queryset(self) -> QuerySet[Any]:
        category=get_object_or_404(Category,pk=self.kwargs['pk'])
        return Article.objects.filter(category=category)   
        
class CategoryUpdateView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,UpdateView):
    model=Category
    login_url=reverse_lazy('user-login')
    template_name='article/category_update_form.html'
    fields='__all__'
    success_url=reverse_lazy('category-list')

class CategoryDeleteView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,DeleteView):
    model=Category
    login_url=reverse_lazy('user-login')
    success_url=reverse_lazy('category-list')

class PurepageCreateView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,CreateView):
    model=Purepage
    login_url=reverse_lazy('user-login')
    template_name='article/purepage_create_form.html'
    fields=['title','content']
    success_url=reverse_lazy('pure-page-list')

#NOTE:静态页面没有作者栏显示,也没有静态页面详情,后续可以看情况修正
    def form_valid(self, form):
        form.instance.auther=self.request.user
        return super().form_valid(form)
    

class PurepageUpdateView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,UpdateView):
    model=Purepage
    login_url=reverse_lazy('user-login')
    template_name='article/purepage_update_form.html'
    success_url=reverse_lazy('pure-page-list')
    fields=['title','content']
    context_object_name='page'

class PurepageDeleteView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,DeleteView):
    model=Purepage
    login_url=reverse_lazy('user-login')
    success_url=reverse_lazy('pure-page-list')
    #静态文章谁都可以删就不做要求了

class PurepageListView(LoginRequiredMixin,AjaxResponseMixin,ListView):
    model=Purepage
    login_url=reverse_lazy('user-login')
    template_name='article/purepage_list.html'
    context_object_name='page_list'

@method_decorator(csrf_exempt,name='dispatch')
@method_decorator(xframe_options_exempt, name='post')
class ImageUpload(View):
    def post(self,request):
        image_obj=request.FILES.get('imgFile')
        if not image_obj:
            return JsonResponse({'error':1,'message':"数据丢失,请重试"})
        else:
            storage=default_storage
            file_suffix=os.path.splitext(image_obj.name)[-1]
            today_time=datetime.today()
            sub_file_name=f"uploads/{today_time.strftime('%Y%m%d')}/{uuid4().hex[:8]}{file_suffix.lower()}"
            
            storage.save(os.path.join(settings.MEDIA_ROOT,sub_file_name),image_obj)
            return JsonResponse({'error':0,'url':posixpath.join(settings.MEDIA_URL,sub_file_name)})
    