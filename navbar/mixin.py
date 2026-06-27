from django.views.generic import TemplateView
from .models import NavbarItem
class NavbarMixin(TemplateView):
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        nav_item_list=NavbarItem.objects.all()
        context['nav_item_list']=nav_item_list
        return context