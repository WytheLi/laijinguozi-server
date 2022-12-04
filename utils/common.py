from decimal import Decimal


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
