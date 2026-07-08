from typing import Any
from .models import LinkItem
from django.views.generic.base import ContextMixin
class LinkItemMixin(ContextMixin):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        context['link_list']=LinkItem.objects.all()
        return context
