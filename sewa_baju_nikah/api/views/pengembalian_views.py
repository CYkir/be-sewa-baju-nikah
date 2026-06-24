from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import date
from sewa_baju_nikah_app.models import TransaksiSewa,DetailTransaksiSewa
from api.permissions.role_permissions import IsKasirPermission
class PengembalianAPIView(APIView):
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

        if transaksi.status_sewa == 'DIKEMBALIKAN':
            return JsonResponse({
                'success': False,
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Baju sudah dikembalikan',
            }, status=status.HTTP_400_BAD_REQUEST)

        detail_transaksi = DetailTransaksiSewa.objects.filter(
            transaksi=transaksi
        )

        for item in detail_transaksi:
            baju = item.baju
            baju.stok += item.qty

            # STATUS TERSEDIA
            if baju.stok > 0:
                baju.status_ketersediaan = (
                    'TERSEDIA'
                )
            baju.save()

        transaksi.status_sewa = 'DIKEMBALIKAN'
        transaksi.tanggal_dikembalikan = (
            date.today()
        )
        transaksi.save()

        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Baju berhasil dikembalikan',
            'data': {
                'kode_transaksi'        : (transaksi.kode_transaksi),
                'nama_penyewa'          : (transaksi.penyewa.nama_penyewa),
                'tanggal_dikembalikan'  : (transaksi.tanggal_dikembalikan),
                'status_sewa'           : (transaksi.status_sewa)
            }

        }, status=status.HTTP_200_OK)