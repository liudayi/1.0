from typing import Any
from django.views.generic.base import ContextMixin
from django.db.models import Count
from .models import Article,Category
class ArticleMixinView(ContextMixin):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['article_list']=Article.objects.select_related('category').all()
        return context
    
class CategoryMixin(ContextMixin):
    def get_context_data(self, **kwargs) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            context["category_list"] = Category.objects.annotate(blog_number=Count('article'))
            #count()里写的是 反向查询传送门的名字,即关联模型名小写或related_name=''
            return context