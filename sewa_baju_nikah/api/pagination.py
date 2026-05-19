# from collections import OrderedDict
# from rest_framework import pagination
# from rest_framework.pagination import LimitOffsetPagination

# class CustomPagination(LimitOffsetPagination):
#   default_limit = 10
#   limit_query_param = 'limit'
#   offset_query_param = 'offset'
#   min_limit = 1
#   max_limit = 50
#   min_offset = 0
#   max_offset = 10

from rest_framework.pagination import (
    LimitOffsetPagination
)

from rest_framework.response import Response


class CustomPagination(
    LimitOffsetPagination
):

    default_limit = 10

    limit_query_param = 'limit'

    offset_query_param = 'offset'

    max_limit = 50

    # =============================================
    # CUSTOM RESPONSE PAGINATION
    # =============================================

    def get_paginated_response(
        self,
        data
    ):

        return Response({
            'success': True,
            'status': 200,
            'message': 'Data berhasil diambil',
            'pagination': {
                'total_data': self.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'limit': self.limit,
                'offset': self.offset,
            },
            'data': data['data']
        })