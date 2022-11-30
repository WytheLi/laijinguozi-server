import os
import sys
import time
from pathlib import Path

import django

base_path = Path(__file__).resolve().parent.parent

sys.path.insert(0, base_path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "laijinguozi.settings")     # 加载django的环境变量
django.setup()  # 将django环境生效

from users.models import Users
from goods.models import GoodsCategory, Store, Brand, GoodsUnit


def create_super_user():
    # result = Users.objects.get_or_create(username="admin",
    #                                      defaults={"mobile": "18212345678", "is_superuser": True, "is_employee": True})
    # 普通的创建记录创建超级管理员用户，导致admin后台登录不了，使用create_superuser()方法创建
    # from django.contrib.auth.models import UserManager

    if not Users.objects.filter(is_superuser=True).exists():
        Users.objects.create_superuser(username="admin", mobile="18212345678", is_employee=True, password="qwer1234")


def add_goods_category():
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
    :return:
    """
    category_list = [
        {"sequence": 1, "name": "热销爆品"},
        {"sequence": 2, "name": "网红特卖"},
        {"sequence": 3, "name": "葡提梅果"},
        {"sequence": 4, "name": "柑橘橙柚"},
        {"sequence": 5, "name": "苹果蕉梨"},
        {"sequence": 6, "name": "西瓜/蜜瓜"},
        {"sequence": 7, "name": "干果/饮品"},
        {"sequence": 8, "name": "现切/下午茶"},
        {"sequence": 9, "name": "礼盒果篮"},
    ]

    if not GoodsCategory.objects.exists():
        all_goods_category = list()
        for category in category_list:
            goods_category = GoodsCategory(**category)
            all_goods_category.append(goods_category)

        GoodsCategory.objects.bulk_create(all_goods_category)


def add_store():
    Store.objects.get_or_create(name="南湖店")


def add_brand():
    if not Brand.objects.exists():
        Brand.objects.create(name="青怡", first_letter="Q")
        Brand.objects.create(name="红富士", first_letter="Q")


def add_goods_unit():
    units = ["箱", "包", "串"]

    if not GoodsUnit.objects.exists():
        all_goods_unit = []
        for unit in units:
            goods_unit = GoodsUnit(name=unit)
            all_goods_unit.append(goods_unit)

        GoodsUnit.objects.bulk_create(all_goods_unit)


def main():
    create_super_user()
    add_store()
    add_brand()
    add_goods_unit()
    add_goods_category()


if __name__ == '__main__':
    main()
