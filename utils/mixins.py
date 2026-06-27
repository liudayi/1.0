import logging
import traceback

from django.db import transaction
from django.http import JsonResponse

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
        except Exception as e:
            ret={
                'state':'error',
                'msg':"AtomicMixin-dispatch-error"
            }
            logging.error(e)
            ret['msg']="内部处理错误,请将错误信息截图并发送管理员<br/><br/>"+traceback.format_exc().replace('\n','<br/>')
            logging.error("request Exception=\n%s",traceback.format_exc())
            return JsonResponse(ret)