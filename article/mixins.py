from typing import Any
from django.views.generic.base import ContextMixin
from django.db.models import Count
from .models import Category,Article
#CHANGE:用ArticleMixin没法分页
""" class ArticleMixin(ContextMixin):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['article_list']=Article.objects.select_related('category').all()
        return context """
    
class CategoryMixin(ContextMixin):
    def get_context_data(self, **kwargs) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            category_list =list( Category.objects.annotate(blog_number=Count('article')) )
            category_list.append({
                  'id':0,
                  'name':"未分类",
                  'blog_number':Article.objects.filter(category=None).count()
            })
            context['category_list']=category_list
            #count()里写的是 反向查询传送门的名字,即关联模型名小写或related_name=''
            return context