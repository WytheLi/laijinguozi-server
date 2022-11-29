from django.db.models.constants import LOOKUP_SEP
from rest_framework.filters import BaseFilterBackend


class MaterialFilter(BaseFilterBackend):
    """
        物料过滤
    """
    def get_search_fields(self, view, request):
        return getattr(view, 'search_fields', None)

    def get_search_params(self, request):
        return request.query_params

    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_params = self.get_search_params(request)

        for key, value in search_params.items():
            if key in search_fields:
                orm_lookup = LOOKUP_SEP.join([key, 'icontains'])
                queryset = queryset.filter(**{orm_lookup: value})

        return queryset
