from django.db import models

# Create your models here.


class Province(models.Model):
    """省"""
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'example_province'
        verbose_name = '省份'
        verbose_name_plural = verbose_name


class City(models.Model):
    """市"""
    name = models.CharField(max_length=5)
    province = models.ForeignKey(Province, models.PROTECT, related_name='cities', verbose_name='省份')

    class Meta:
        db_table = 'example_city'
        verbose_name = '城市'
        verbose_name_plural = verbose_name


class Person(models.Model):
    """人"""
    name = models.CharField(max_length=10)
    visitation = models.ManyToManyField(City, related_name="visitor", verbose_name='旅游过的城市')
    hometown = models.ForeignKey(City, models.PROTECT, related_name="birth", verbose_name='出生城市')
    living = models.ForeignKey(City, models.PROTECT, related_name="citizen", verbose_name='居住城市')

    class Meta:
        db_table = 'example_person'
        verbose_name = '人'
        verbose_name_plural = verbose_name
