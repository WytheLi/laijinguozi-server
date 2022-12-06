from django.db import models

# Create your models here.


class Areas(models.Model):
    """
    行政区划
    """
    name = models.CharField(max_length=32, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subs', null=True, blank=True, verbose_name='上级行政区划')
    short_name = models.CharField(max_length=8, verbose_name='简称')
    level_type = models.SmallIntegerField(verbose_name='级别:0,中国；1，省分；2，市；3，区、县')
    city_code = models.CharField(max_length=8, verbose_name='城市代码')
    postcode = models.CharField(max_length=6, verbose_name='邮编')
    lng = models.CharField(max_length=16, verbose_name='经度')
    lat = models.CharField(max_length=16, verbose_name='纬度')
    pinyin = models.CharField(max_length=32, verbose_name='拼音')
    status = models.BooleanField(default=1, verbose_name='状态')

    class Meta:
        db_table = 'fruits_areas'
        verbose_name = '省-市-区行政区划'
        verbose_name_plural = verbose_name
