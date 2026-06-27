from datetime import datetime
import os,posixpath
from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
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
# Create your views here.

class BlogListView(LoginRequiredMixin,ListView):
    #对应的前端页面没有作者,因为文章创建者就是作者自己?每个用户只能管理自己的文章?
    #不,我觉得就是单纯没有写()我记得他在删除类里有做限制,每个人只能删除自己写的文章
    model=Article
    login_url=reverse_lazy('user-login')
    """ context_object_name='essay_list' """
    template_name='article/blog_list.html'#后台

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['essay_list']=Article.objects.select_related('category').all()
        return context

class BlogCreateView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,CreateView):
    model=Article
    login_url=reverse_lazy('user-login')
    fields=['title','category','summary','content']#editor_id是富文本编辑器的意思
    success_url=reverse_lazy('blog-list-backend')
    #还要添加图片#额外写image_upload类适配
    template_name='article/blog_create_form.html'

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

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['blog']=self.object
        context['category_list']=Category.objects.all()
        return context

    
class BlogDeleteView(LoginRequiredMixin,AtomicMixin,AjaxResponseMixin,DeleteView):
    model=Article
    login_url=reverse_lazy('user-login')
    success_url='blog-list-backend'

from navbar.mixin import NavbarMixin
from link.mixins import LinkItemMixin
from mood.mixin import MoodMixin
from article.mixins import ArticleMixinView,CategoryMixin

class ArticleDetailView(CategoryMixin,ArticleMixinView,MoodMixin,LinkItemMixin,NavbarMixin,LoginRequiredMixin,AjaxResponseMixin,DetailView):
    model=Article
    login_url=reverse_lazy('user-login')
    template_name='article/article_detail.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if not hasattr(self,'object') or self.object is None:
            self.object=self.get_object()
        self.object.show_times+=1
        self.object.save(update_fields=['show_times'])
        context=super().get_context_data(**kwargs)
        context['article']=self.object
        return context
        


class ArticleListView(LoginRequiredMixin,AjaxResponseMixin,ListView):
    model=Article
    login_url=reverse_lazy('user-login')
    template_name='article/article_list.html'#前台

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

class CategoryWeightView(CategoryListView):
    template_name='article/category_weight.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            context["category_list"] = Category.objects.annotate(blog_number=Count('article'))
            #count()里写的是 反向查询传送门的名字,即关联模型名小写或related_name=''
            return context
        
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

#TODO:静态页面没有作者栏显示,也没有静态页面详情,后续可以看情况修正
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
    