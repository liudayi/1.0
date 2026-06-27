from django.db import models

# Create your models here.
class LinkItem(models.Model):
    title=models.CharField(max_length=50,verbose_name='友链标题')
    order=models.IntegerField(verbose_name='展示顺序',null=False)
    url=models.CharField(max_length=300,verbose_name='指向链接')
    description=models.TextField(max_length=200,verbose_name="链接描述")

    def __str__(self) -> str:
        return f"title={self.title},url={self.url},说明={self.description},order={self.order}"

    class Meta:
        ordering=['order']