from django.db import models

# Create your models here.


class Area(models.Model):
    """
    行政区划
    """
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subs', null=True, blank=True, verbose_name='上级行政区划')
    postcode = models.CharField(max_length=6, null=True, blank=True, verbose_name='邮政编码')

    class Meta:
        db_table = 'fruits_areas'
        verbose_name = '省-市-区行政区划'
        verbose_name_plural = verbose_name
