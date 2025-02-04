from rest_framework import pagination
from rest_framework.response import Response


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = 'limit'
    max_page_size = 100


class Pagination:
    @property
    def paginator(self):
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class PaginationMethod(Pagination):

    def page(self, instance, serializers, request):
        page = super().paginate_queryset(instance)
        if page is not None:
            serializer = super().get_paginated_response(
                serializers(page, many=True, context={'request': request}).data
            )
        else:
            serializer = serializers(instance, many=True, context={'request': request})
        return serializer


# class PageSortNumberPagination(pagination.PageNumberPagination):
#
#     def get_paginated_response(self, data):
#         return Response({
#             'count': self.page.paginator.count,
#             'next': self.get_next_link(),
#             'previous': self.get_previous_link(),
#             'results': data,
#             'sort_fields': [],
#             'shop_logo': [],  # TODO
#         })
