import math
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PagePagination(PageNumberPagination):
    """
        自定义分页类

        PageNumberPagination基于Django Paginator封装。
    """
    page_size = 10  # 每页的数据量（默认）
    page_query_param = "page_index"
    page_size_query_param = "page_size"
    max_page_size = 20  # 每页最大数量，请求参数中如果超过了这个配置，不会报错，会按照此配置工作

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('pagination', OrderedDict([
                ('total', self.page.paginator.count()),
                ('current_page', self.page.number),
                ('page_size', self.page.paginator.per_page),
                ('page_total', math.ceil(self.page.paginator.count / self.page.paginator.per_page))
            ])),
            ('items', data)
        ]))
