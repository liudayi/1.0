from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView,ListView
from utils.mixins import FrontMixin
from article.models import Article
# Create your views here.
class HomepageView(FrontMixin,ListView):
    template_name='website/frontend/homepage.html'
    model=Article
    context_object_name='article_list'
    paginate_by=5

class DashboardView(TemplateView):
    template_name='website/backend/overview.html'
    
    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     context=super().get_context_data(**kwargs)
    #     print(self.request.META.get('HTTP_USER_AGENT'))#不同浏览器返回的字符串可能会有大小写差异
    #     return context
#Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:148.0) Gecko/20100101 Firefox/148.0

#Mozilla/5.0 (iPhone; CPU iPhone OS 18_6 like Mac OS X) 
# AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Mobile/15E148 Safari/604.1

#Mozilla/5.0 (Linux; Android 14; SM-S938B) 
# AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36
