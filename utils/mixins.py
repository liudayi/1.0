import logging
import traceback

from django.db import transaction
from django.http import Http404, JsonResponse

from navbar.mixin import NavbarMixin
from link.mixins import LinkItemMixin
from mood.mixin import MoodMixin
from article.mixins import CategoryMixin

class FrontMixin(NavbarMixin,LinkItemMixin,MoodMixin,CategoryMixin):
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class AjaxResponseMixin(object):
    def form_invalid(self,form):
        response= super().form_invalid(form)
        if self.request.headers.get('x-requested-with')=='XMLHttpRequest':
            data={
                'state':'error',
                'msg':form.errors.as_text()+"AjaxResponseMixin-form_invalid-error"
            }
            logging.error(form.errors)
            return JsonResponse(data,status=400)
        else:
            return response
        
    def form_valid(self,form):
        response=super().form_valid(form)
        if self.request.headers.get('x-requested-with')=='XMLHttpRequest':
            data={
                'state':'success',
            }
            return JsonResponse(data)
        else:
            return response
    
class AtomicMixin(object):
    def dispatch(self,request,*args,**kwargs):
        try:
            with transaction.atomic():
                return super().dispatch(request,*args,**kwargs)
        except Http404:
            # 2. 【核心新增】如果是越权或找不到引发的 404 异常，直接原样往上抛 (raise)
            # 这样就能绕过下面的通用 Exception 拦截，让 Django 官方中间件接管并渲染 404 页面
            raise
        except Exception as e:
            ret={
                'state':'error',
                'msg':"AtomicMixin-dispatch-error"
            }
            logging.error(e)
            ret['msg']="内部处理错误,请将错误信息截图并发送管理员<br/><br/>"+traceback.format_exc().replace('\n','<br/>')
            logging.error("request Exception=\n%s",traceback.format_exc())
            return JsonResponse(ret)
        
