import os

from django.http import JsonResponse
from django.conf import settings

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated
)

from reportlab.pdfgen import canvas

from sewa_baju_nikah_app.models import (
    TransaksiSewa
)

from api.permissions.role_permissions import (
    IsAdminOrKasirPermission
)


class CetakStrukAPIView(APIView):

    def get_permissions(self):

        return [
            IsAuthenticated(),
            IsAdminOrKasirPermission()
        ]

    def get(self, request, pk):

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

        folder_path = os.path.join(
            settings.MEDIA_ROOT,
            'struk'
        )
        os.makedirs(
            folder_path,
            exist_ok=True
        )
        file_name = (
            f"struk_"
            f"{transaksi.kode_transaksi}.pdf"
        )

        file_path = os.path.join(
            folder_path,
            file_name
        )

        # Generate PDF
        pdf = canvas.Canvas(file_path)

        pdf.setFont(
            'Helvetica-Bold',
            16
        )
        pdf.drawString(
            180,
            800,
            'SEWA BAJU NIKAH'
        )

        # DETAIL TRANSAKSI

        pdf.setFont(
            'Helvetica',
            12
        )
        pdf.drawString(
            50,
            760,
            f'Kode : {transaksi.kode_transaksi}'
        )

        pdf.drawString(
            50,
            740,
            f'Nama Penyewa : '
            f'{transaksi.penyewa.nama_penyewa}'
        )

        pdf.drawString(
            50,
            720,
            f'Tanggal Sewa : '
            f'{transaksi.tanggal_sewa}'
        )

        pdf.drawString(
            50,
            700,
            f'Tanggal Kembali : '
            f'{transaksi.tanggal_kembali}'
        )

        # DETAIL BAJU
        y = 660
        for detail in transaksi.detail_transaksi.all():
            pdf.drawString(
                50,
                y,
                f'{detail.baju.nama_baju}'
            )

            pdf.drawString(
                300,
                y,
                f'Qty : {detail.qty}'
            )

            pdf.drawString(
                400,
                y,
                f'Rp {detail.subtotal}'
            )

            y -= 20

        # TOTAL
        y -= 20

        pdf.setFont(
            'Helvetica-Bold',
            12
        )

        pdf.drawString(
            50,
            y,
            f'Total : Rp '
            f'{transaksi.total_bayar}'
        )

        # FOOTER
        y -= 40

        pdf.setFont(
            'Helvetica',
            11
        )
        pdf.drawString(
            50,
            y,
            'Terima kasih telah menyewa'
        )
        # SAVE PDF
        pdf.showPage()
        pdf.save()

        # PDF URL

        pdf_url = request.build_absolute_uri(

            settings.MEDIA_URL +
            'struk/' +
            file_name

        )
        # RESPONSE JSON
        return JsonResponse({

            'success': True,

            'status': status.HTTP_200_OK,

            'message': 'Struk berhasil dibuat',

            'data': {

                'kode_transaksi': (
                    transaksi.kode_transaksi
                ),

                'url_struk': pdf_url

            }

        }, status=status.HTTP_200_OK)