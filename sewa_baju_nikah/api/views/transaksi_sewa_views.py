from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from sewa_baju_nikah_app.models import (
    TransaksiSewa
)
from api.serializers.transaksi_sewa_serializers import (
    TransaksiSewaSerializer
)
from api.permissions.role_permissions import (
    IsAdminOrKasirPermission, IsAdminPermission, IsKasirPermission
)
from api.utils.transaction_helper import (
    generate_kode_transaksi
)

import django_filters.rest_framework
from api.pagination import CustomPagination
from rest_framework.filters import (
    OrderingFilter
)
class TransaksiSewaAPIView(APIView):
    def get_permissions(self):
      if self.request.method == 'GET':
        return [
          IsAuthenticated(),
          IsAdminOrKasirPermission()
        ]
      return [
            IsAuthenticated(),
            IsKasirPermission()
        ]

    def get(self, request):
        transaksi = TransaksiSewa.objects.filter(
            status_data='AKTIF'
        ).order_by('-id')
        serializer = TransaksiSewaSerializer(
            transaksi,
            many=True
        )

        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Data transaksi berhasil diambil',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data['kode_transaksi'] = (
            generate_kode_transaksi()
        )
        serializer = TransaksiSewaSerializer(
            data=data
        )
        if serializer.is_valid():
            serializer.save(
                created_by=request.user
            )

            return JsonResponse({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'message': 'Transaksi berhasil dibuat',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Transaksi gagal dibuat',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

class TransaksiSewaFilterApi(generics.ListAPIView):
    queryset = TransaksiSewa.objects.all()
    serializer_class = TransaksiSewaSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status_sewa']
    ordering_fields = ['created_at', 'harga_sewa',]

