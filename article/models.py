from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
#三个类+一个抽象基类:category文章分类purepage静态页面article文章base_article抽象基类
class base_article(models.Model):
    title=models.CharField(verbose_name=("标题"), max_length=50)
    author=models.ForeignKey(User,verbose_name="作者",on_delete=models.SET_NULL,null=True,blank=True)
    content=models.TextField(verbose_name="内容")
    publish_time=models.DateTimeField(auto_now_add=True,verbose_name="发布时间")
    modification_time=models.DateTimeField(auto_now=True,verbose_name="修改时间")
    
    
    class Meta:
        abstract=True
    
class Category(models.Model):
    name=models.CharField(max_length=50,default="未分类",verbose_name="类别名称")

    """ @property
    def blog_number(self):
        return self.article_set.count()
    #{{ category.blog_number }}会触发前端的n+1查询,不推荐 """
    
    def __str__(self) -> str:
        return f"{self.name}"

class Purepage(base_article):

    """ @property
    def get_absolute_url(self):
        return reverse("blog-detail", kwargs={'pk':self.pk}) """

class Article(base_article):
    #image=models.ImageField(upload_to="",blank=True,null=True,verbose_name='图片')
    category=models.ForeignKey(Category,null=True,blank=True,on_delete=models.SET_NULL)#分类下有文章时不可删
    show_times=models.IntegerField(verbose_name="查看次数",default=0)
    summary=models.TextField(verbose_name="摘要")
    
    """ @property
    def get_category_name(self):
        #print(self.category.name)
        return self.category.name if self.category.name else "未分类"
    
    @property
    def safe_category_id(self):
        return self.category.id if self.category.id else 0
 """