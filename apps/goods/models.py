from decimal import Decimal

from django.db import models
from utils.models import BaseModel

# Create your models here.


class GoodsCategory(BaseModel):
    """
        1、热销爆品
        2、网红特卖
        3、葡提梅果
        4、柑橘橙柚
        5、苹果蕉梨
        6、西瓜/蜜瓜
        7、干果/饮品
        8、现切/下午茶
        9、礼盒果篮
    """
    name = models.CharField(max_length=6, verbose_name='品类')
    sequence = models.SmallIntegerField(unique=True, verbose_name='序号')

    class Meta:
        db_table = 'fruits_goods_category'
        verbose_name = '商品品类'
        verbose_name_plural = verbose_name


class Brand(BaseModel):
    name = models.CharField(max_length=20, verbose_name='名称')
    logo = models.TextField(verbose_name='Logo图片')
    first_letter = models.CharField(max_length=1, verbose_name='品牌首字母')

    class Meta:
        db_table = 'fruits_brand'
        verbose_name = '品牌'
        verbose_name_plural = verbose_name


class GoodsUnit(BaseModel):
    name = models.CharField(max_length=2, verbose_name='单位名，英文全转换为大写')

    class Meta:
        db_table = 'fruits_goods_unit'
        verbose_name = '单位'
        verbose_name_plural = verbose_name


class Store(BaseModel):
    name = models.CharField(max_length=16, verbose_name='店名')

    class Meta:
        db_table = 'fruits_store'
        verbose_name = '店铺'
        verbose_name_plural = verbose_name


class Material(BaseModel):
    """
        物料，商品的基本信息
    """
    code = models.CharField(max_length=32, verbose_name='商品编码')
    name = models.CharField(max_length=16, verbose_name='商品名称')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='品牌')
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='goods_category', verbose_name='类别')
    unit = models.ForeignKey(GoodsUnit, models.PROTECT, related_name='goods_unit', verbose_name='单位')
    spec = models.CharField(max_length=8, verbose_name='规格')
    origin = models.CharField(max_length=8, verbose_name='产地')
    images = models.TextField(verbose_name='图片')  # 主图.jpg,副图1.jpg,副图2.jpg
    description = models.TextField(verbose_name='商品描述')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'fruits_material'
        verbose_name = '物料'
        verbose_name_plural = verbose_name


class Goods(BaseModel):
    """
        上架到某个门店销售的商品
    """
    material = models.ForeignKey(Material, models.PROTECT, related_name='material', verbose_name='物料')
    original_price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='原价')
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name='特价')
    k = models.SmallIntegerField(default=1, verbose_name='积分系数')     # 会员日3倍积分，周末2倍积分，100积分抵扣一元
    sales_volume = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='销量')
    comments = models.IntegerField(default=0, verbose_name='评论数量')
    maximum_purchase = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='最大购买数')
    minimum_purchase = models.DecimalField(max_digits=4, decimal_places=2, default=Decimal('0.00'), verbose_name='最小购买数')
    state = models.SmallIntegerField(choices=((1, '已上架'), (2, '待审核'), (3, '已下架')), verbose_name='状态')
    store = models.ForeignKey(Store, models.PROTECT, verbose_name='店铺')

    class Meta:
        db_table = 'fruits_goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class Stock(BaseModel):
    goods = models.ForeignKey(Goods, models.CASCADE, verbose_name='商品')
    stock = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='可用库存')
    lock_stock = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='占用库存')

    class Meta:
        db_table = 'fruits_stock'
        verbose_name = '库存'
        verbose_name_plural = verbose_name


class GoodsComment(BaseModel):
    """
        评论，附图评价送积分
    """
    goods = models.ForeignKey(Goods, models.CASCADE, verbose_name='商品')
    score = models.IntegerField(default=10, verbose_name='每两分为一星，10分为五星')
    reviews = models.TextField(verbose_name='评语')
    images = models.TextField(verbose_name='图片，多张图片","分割')

    class Meta:
        db_table = 'fruits_goods_comment'
        verbose_name = '评价'
        verbose_name_plural = verbose_name
