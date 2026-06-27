from typing import Iterable
from django.db import models

# Create your models here.
class NavbarItem(models.Model):
    title=models.CharField(max_length=50,verbose_name="导航项")
    url=models.CharField(max_length=100,verbose_name="指向地址")
    order=models.IntegerField(verbose_name="权重",null=True)

    def __str__(self) -> str:
        return f"title={self.title},url={self.url},order={self.order}"
    
    def save(self,*args,**kwargs) -> None:
        flag=self.id is None
        super().save(*args,**kwargs)

        if flag and self.order is None:
            self.order=self.id
            super().save(update_fields=['order'])

    class Meta:
        ordering=['order']
        verbose_name="导航栏"

    