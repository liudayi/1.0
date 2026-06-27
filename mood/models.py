from datetime import datetime
import os
from uuid import uuid4
from django.db import models

# Create your models here.
class Mood(models.Model):
    
    def mood_image_path(instance,filename):
        ext=filename.split('.')[-1]#获取文件名后缀
        filename=f'{datetime.now().strftime("%Y/%m/%d_%H%M%S")}.{ext}'
        return os.path.join('mood',filename)
    
    type_choice=[
        ('T',"文字"),
        ('I',"图文"),
        ('B',"引用")
    ]

    title=models.CharField(verbose_name='标题',max_length=100)
    create_time=models.DateTimeField(auto_now_add=True,verbose_name="发布时间")
    content=models.TextField(verbose_name='内容')
    image=models.ImageField(upload_to=mood_image_path,null=True,blank=True,verbose_name='配图')
    mood_type=models.CharField(verbose_name='类型',choices=type_choice,max_length=10)
    #get_small_image_url=models.URLField(verbose_name='图片链接')

    def __str__(self) -> str:
        return f"标题={self.title},类型={self.get_mood_type_display},发布时间={self.create_time},内容={self.content},动作={self.mood_type}"   

    class Meta:
        ordering=['-create_time']
    # 在 models.py 的 class Mood(models.Model) 内部添加：

    def get_small_image_url(self):
        """获取图片路径，做好防御性编程"""
        if self.image:
            return self.image.url
        else:
            # 如果不小心漏传了图，返回一张默认的占位图，防止前端页面崩裂
            from django.conf import settings
            return f"{settings.STATIC_URL}images/default_mood.jpg"