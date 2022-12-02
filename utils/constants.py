from enum import Enum, unique


class GoodsState(Enum):
    ON_SALE = 1     # 售卖中（已上架）
    UN_CHECKED = 2    # 待审核
    NO_PASS = 3     # 不通过
    APPROVE = 4     # 审核通过
    UN_SALE = 5     # 已下架
    DRAFT = 6       # 草稿

    SOLD = [ON_SALE, UN_SALE]   # 销售过（包括销售中）
    CHECKED = [APPROVE, NO_PASS]    # 经过审批的


class OrderState(Enum):
    FINISH = 1      # 已完成
    UNPAID = 2      # 待支付
    CANCELED = 3    # 已取消
    UN_DELIVER = 4  # 待配送


@unique
class RequestType(Enum):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'
    PUT = 'PUT'
    DELETE = 'DELETE'


class DeliverType(Enum):
    HOME_DELIVERY = 1       # 送货上门
    SELF_PICKUP = 2         # 自提
    EXPRESS = 3             # 快递
