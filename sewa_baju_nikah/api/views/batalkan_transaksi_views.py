from django.http import JsonResponse
from django.db import transaction

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from sewa_baju_nikah_app.models import (
    TransaksiSewa,
    DetailTransaksiSewa
)

from api.permissions.role_permissions import (
    IsKasirPermission
)


class BatalkanTransaksiAPIView(APIView):

    def get_permissions(self):
        return [
            IsAuthenticated(),
            IsKasirPermission()
        ]

    @transaction.atomic
    def post(self, request, pk):
        try:
            transaksi = TransaksiSewa.objects.select_for_update().get(
                pk=pk,
                status_data='AKTIF'
            )
        except TransaksiSewa.DoesNotExist:
            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Transaksi tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)

        if transaksi.status_sewa == 'DIBATALKAN':
            return JsonResponse({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Transaksi sudah dibatalkan',
            }, status=status.HTTP_400_BAD_REQUEST)

        if transaksi.status_sewa != 'DIPROSES':
            return JsonResponse({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Transaksi hanya bisa dibatalkan jika status masih DIPROSES',
            }, status=status.HTTP_400_BAD_REQUEST)

        detail_transaksi = DetailTransaksiSewa.objects.filter(
            transaksi=transaksi
        )

        for item in detail_transaksi:
            baju = item.baju
            baju.stok += item.qty

            if baju.stok > 0:
                baju.status_ketersediaan = 'TERSEDIA'

            baju.save()

        transaksi.status_sewa = 'DIBATALKAN'
        transaksi.save()

        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Transaksi berhasil dibatalkan dan stok baju dikembalikan',
            'data': {
                'id': transaksi.id,
                'kode_transaksi': transaksi.kode_transaksi,
                'nama_penyewa': transaksi.penyewa.nama_penyewa,
                'status_sewa': transaksi.status_sewa,
            }
        }, status=status.HTTP_200_OK)