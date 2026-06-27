from typing import Any
from .models import Mood

class MoodMixin(object):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context=super().get_context_data(**kwargs)
        new_mood=Mood.objects.first()#应该只返回一个
        if new_mood:
            context['mood']=new_mood
        return context