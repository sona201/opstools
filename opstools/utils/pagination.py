from rest_framework.pagination import PageNumberPagination


class GlobalPagination(PageNumberPagination):
    page_query_param = 'page'  # 前端发送的页数关键字名，默认为page
    page_size = 10  # 每页数目
    page_size_query_param = 'size'  # 前端发送的每页数目关键字名，默认为None
    max_page_size = 1000  # 前端最多能设置的每页数量

# 当特殊情况需要所有数据，又不想用分页来获取时，可以去除分页，在 viewset 里
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         # 使用 pagination_class = None 为全局不分页
#         # 加下判断可以在使用参数的方式两种方式都用起来
#         if not request.query_params.get('is_all') == 'true':
#             page = self.paginate_queryset(queryset)
#             if page is not None:
#                 serializer = self.get_serializer(page, many=True)
#                 return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(queryset, many=True)
#         # 返回的数据结构统一都是 data.result
#         result = {
#             "count": len(queryset),
#             "results": serializer.data
#         }
#         return Response(result)
