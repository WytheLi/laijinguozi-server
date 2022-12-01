from enum import Enum


class GoodsState(Enum):
    ON_SALE = 1     # 售卖中（已上架）
    UN_CHECKED = 2    # 待审核
    NO_PASS = 3     # 不通过
    APPROVE = 4     # 审核通过
    UN_SALE = 5     # 已下架
    DRAFT = 6       # 草稿

    SOLD = [ON_SALE, UN_SALE]   # 销售过（包括销售中）
    CHECKED = [APPROVE, NO_PASS]    # 经过审批的
