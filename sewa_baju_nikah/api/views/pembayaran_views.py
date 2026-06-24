from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
)
from sewa_baju_nikah_app.models import (
    Pembayaran
)
from api.serializers.pembayaran_serializers import (
    PembayaranSerializer
)

from api.permissions.role_permissions import (
    IsAdminPermission, IsKasirPermission
)
class PembayaranAPIView(APIView):
    def get_permissions(self):
      if self.request.method == 'GET':
        return [
          IsAuthenticated(),
          IsAdminPermission()
        ]
      return [
            IsAuthenticated(),
            IsKasirPermission()
        ]

    def get(self, request):
        pembayaran = Pembayaran.objects.filter(
            status_data='AKTIF'
        ).order_by('-id')
        serializer = PembayaranSerializer(
            pembayaran,
            many=True
        )
        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Data pembayaran berhasil diambil',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PembayaranSerializer(
            data=request.data,
            context={
                'request': request
            }
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'message': 'Pembayaran berhasil dilakukan',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return JsonResponse({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Pembayaran gagal dilakukan',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)