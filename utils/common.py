from decimal import Decimal

from goods.models import Stock


class Apportion(object):

    def __init__(self, unallocated: Decimal, allocation_base: Decimal, counter: int):
        """
            分摊
        :param unallocated: 待摊 <例：红包5元待摊>
        :param allocation_base: 分摊基数 <例：sum(单价*数量 - 不参与分摊的金额)>
        :param counter: 待摊次数 <例：订单明细中5个单品，3个参与分摊，待摊次数为3>
        """
        self.unallocated = unallocated
        self.surplus_unallocated = unallocated
        self.counter = counter
        self.allocation_base = allocation_base

    def calc_should_divided(self, allocation_value: Decimal):
        """
            计算应分摊的数值
        :param allocation_value: 单品参与分摊的金额 <例：单价*数量 - 不参与分摊的金额>
        :return:
        """
        if self.unallocated <= 0:
            return 0

        if self.counter == 1:   # 由于精度问题，最后一次分摊不按比例计算，直接取剩余值
            return self.surplus_unallocated
        else:
            rate = allocation_value / self.allocation_base
            value = self.unallocated * rate

            self.surplus_unallocated -= value
            self.counter -= 1
            return value


class StockControl(object):

    def __init__(self, stock_id, warehouse_id=None):
        """
            库存管理
            库存不仅需要处理增减问题，库存表属于多方操作的表，固然每次更新的时候需要加锁，否则会因为修改脏读的数据而造成数据不准
        :param stock_id: 库存id
        :param warehouse_id: 仓库id
        """
        self.stock_id = stock_id
        self.warehouse_id = warehouse_id

    def update_stock(self, stock, lock_stock):
        """
            更新库存
        :param stock: 需要增减的库存数量，减为负数
        :param lock_stock: 需要锁定、释放锁定的库存数量，减为负数
        :return:
        """
        queryset = Stock.objects.select_for_update().filter(id=self.stock_id)

        if self.warehouse_id:
            queryset = queryset.filter(warehouse_id=self.warehouse_id)

        instance = queryset.first()
        instance.stock += stock
        instance.lock_stock += lock_stock
        instance.save()
