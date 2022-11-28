from django.db import models


class BaseModel(models.Model):
    """为模型类补充字段"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    # create_uid = models.ForeignKey('Users', models.SET_NULL, null=True, blank=True, related_name='create_uid')
    # update_uid = models.ForeignKey('Users', models.SET_NULL, null=True, blank=True, related_name='update_uid')

    class Meta:
        abstract = True  # 说明是抽象模型类, 用于继承使用，数据库迁移时不会创建BaseModel的表

    def __str__(self):
        name = getattr(self, 'name')
        if name:
            return '%s: (%s, %s)' % (self.__class__.__name__, self.pk, name)
        else:
            return '%s: (%s)' % (self.__class__.__name__, self.pk)
