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


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='PersonGroupRelation')

    class Meta:
        db_table = "example_group"
        verbose_name = "用户组"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PersonGroupRelation(models.Model):
    person = models.ForeignKey(Person, models.CASCADE, db_constraint=False)     # db_constraint=False，保留跨表查询的便利(双下划线跨表查询)，数据库不建立外键约束，在业务层校验数据确保数据准确
    group = models.ForeignKey(Group, models.CASCADE, db_constraint=False)
    date_joined = models.DateField()  # 进组日期
    invite_reason = models.CharField(max_length=64)  # 邀请原因

    class Meta:
        db_table = "example_person_group_rel"
        verbose_name = '用户与用户组关联表'
        verbose_name_plural = verbose_name

