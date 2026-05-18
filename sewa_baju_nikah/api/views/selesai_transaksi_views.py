from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated
)

from sewa_baju_nikah_app.models import (
    TransaksiSewa
)

from api.permissions.role_permissions import (
    IsKasirPermission
)

class SelesaikanTransaksiAPIView(APIView):
    def get_permissions(self):

        return [
            IsAuthenticated(),
            IsKasirPermission()
        ]
    def post(self, request, pk):
        try:
            transaksi = TransaksiSewa.objects.get(
                pk=pk,
                status_data='AKTIF'
            )
        except TransaksiSewa.DoesNotExist:
            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Transaksi tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)

        # VALIDASI
        if transaksi.status_sewa != 'DIKEMBALIKAN':
            return JsonResponse({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'message': (
                    'Transaksi belum dikembalikan'
                ),

            }, status=status.HTTP_400_BAD_REQUEST)

        # UPDATE STATUS
        transaksi.status_sewa = 'SELESAI'
        transaksi.save()
        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': (
                'Transaksi berhasil diselesaikan'
            ),
            'data': {
                'kode_transaksi': (transaksi.kode_transaksi),
                'nama_penyewa'  : (transaksi.penyewa.nama_penyewa),
                'status_sewa'   : (transaksi.status_sewa)
            }
        }, status=status.HTTP_200_OK)