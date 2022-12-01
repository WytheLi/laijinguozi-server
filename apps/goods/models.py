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
    logo = models.TextField(null=True, blank=True, verbose_name='Logo图片')
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
    is_enable = models.BooleanField(default=True, verbose_name="启用")

    class Meta:
        db_table = 'fruits_store'
        verbose_name = '店铺'
        verbose_name_plural = verbose_name


class Material(BaseModel):
    """
        物料，商品的基本信息
    """
    code = models.CharField(max_length=32, unique=True, verbose_name='商品编码')
    name = models.CharField(max_length=16, verbose_name='商品名称')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, verbose_name='品牌')
    category = models.ForeignKey(GoodsCategory, on_delete=models.PROTECT, related_name='goods_category', verbose_name='类别')
    purchase_unit = models.ForeignKey(GoodsUnit, models.PROTECT, related_name='purchase_unit', verbose_name='采购单位，例：整件售卖')
    retail_unit = models.ForeignKey(GoodsUnit, models.PROTECT, related_name='retail_unit', verbose_name='零售单位')
    mini_unit = models.ForeignKey(GoodsUnit, models.PROTECT, related_name='mini_unit', null=True, blank=True, verbose_name='最小单位，例：一袋饺子里有20个，`袋`为销售单位，`个`为最小单位')
    retail_unit_weight = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='销售单位换算比例，例：1箱=20包')
    mini_unit_weight = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, verbose_name='最小单位换算比例，例：1包=30串')
    spec = models.CharField(max_length=16, verbose_name='规格')
    origin = models.CharField(max_length=8, verbose_name='产地')
    images = models.TextField(verbose_name='图片')  # 主图.jpg,副图1.jpg,副图2.jpg
    description = models.TextField(verbose_name='商品描述')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        db_table = 'fruits_material'
        verbose_name = '物料'
        verbose_name_plural = verbose_name

    @property
    def spec_text(self):
        """
            根据单位以及换算比例计算规格
        :return:
        """
        # 为了显示友好，换算比例为整数时浮点数转化为整数
        if self.retail_unit_weight is not None and int(self.retail_unit_weight) == self.retail_unit_weight:
            retail_unit_weight = int(self.retail_unit_weight)
        else:
            retail_unit_weight = self.retail_unit_weight

        if self.mini_unit_weight is not None and int(self.mini_unit_weight) == self.mini_unit_weight:
            mini_unit_weight = int(self.mini_unit_weight)
        else:
            mini_unit_weight = self.mini_unit_weight

        return f'1{self.purchase_unit.name}' \
               f'*{retail_unit_weight}{self.retail_unit.name}' \
               f'*{mini_unit_weight}{self.mini_unit.name}' \
                if mini_unit_weight else f'1{self.purchase_unit.name}*{retail_unit_weight}{self.retail_unit.name}'


class Goods(BaseModel):
    """
        上架到某个门店销售的商品
    """
    STATE_CHOICES = (
        (1, '已上架（售卖中）'),
        (2, '待审核'),
        (3, '不通过'),
        (4, '审核通过'),
        (5, '已下架'),
        (6, '草稿')
    )

    material = models.ForeignKey(Material, models.PROTECT, related_name='material', verbose_name='物料')

    whole_piece_price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'), verbose_name='整件价格')
    retail_price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'), verbose_name='零售价格')
    whole_piece_discount_price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'), verbose_name='整件售卖折后价')
    retail_discount_price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'), verbose_name='零售售卖折后价')
    enable_whole_piece = models.BooleanField(default=False, verbose_name='整件售卖')
    enable_retail = models.BooleanField(default=True, verbose_name='零售售卖')

    whole_piece_launched_num = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'), verbose_name='整件起售数量')
    retail_launched_num = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'), verbose_name='零售起售数量')

    has_stock = models.BooleanField(default=False, verbose_name='整件售卖有库存')
    has_stock_retail = models.BooleanField(default=False, verbose_name='零售有库存')

    k = models.SmallIntegerField(default=1, verbose_name='积分系数')     # 会员日3倍积分，周末2倍积分，100积分抵扣一元
    sales_volume = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='销量')
    comments = models.IntegerField(default=0, verbose_name='评论数量')

    state = models.SmallIntegerField(choices=STATE_CHOICES, default=2, verbose_name='状态')
    store = models.ForeignKey(Store, models.PROTECT, verbose_name='店铺')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    latest_shelf_time = models.DateTimeField(null=True, blank=True, verbose_name='最近上架时间')

    class Meta:
        db_table = 'fruits_goods'
        verbose_name = '商品'
        verbose_name_plural = verbose_name


class Stock(BaseModel):
    goods = models.ForeignKey(Goods, models.CASCADE, unique=True, verbose_name='商品')
    stock = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='可用库存')
    lock_stock = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'), verbose_name='占用库存')

    class Meta:
        db_table = 'fruits_stock'
        verbose_name = '库存'
        verbose_name_plural = verbose_name

    @property
    def whole_piece_stock(self):
        """
            换算整件库存
        :return:
        """
        return int(self.stock / self.goods.material.retail_unit_weight)


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
