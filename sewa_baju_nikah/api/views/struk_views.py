import os
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from reportlab.pdfgen import canvas
from sewa_baju_nikah_app.models import TransaksiSewa
from api.permissions.role_permissions import IsAdminOrKasirPermission
class CetakStrukAPIView(APIView):

    def get_permissions(self):
        return [
            IsAuthenticated(),
            IsAdminOrKasirPermission()
        ]
    def get(self, request, pk):
        try:
            transaksi = TransaksiSewa.objects.select_related(
                'penyewa'
            ).prefetch_related(
                'detail_transaksi__baju'
            ).get(
                pk=pk,
                status_data='AKTIF'
            )
        except TransaksiSewa.DoesNotExist:
            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Transaksi tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)

        folder_path = os.path.join(settings.MEDIA_ROOT, 'struk')
        os.makedirs(folder_path, exist_ok=True)

        file_name = f"struk_{transaksi.kode_transaksi}.pdf"
        file_path = os.path.join(folder_path, file_name)

        pdf = canvas.Canvas(file_path)

        width = 595

        # HEADER TOKO
        pdf.setFont('Helvetica-Bold', 20)
        pdf.drawCentredString(width / 2, 810, 'SEWA BAJU NIKAH TRADISIONAL')

        pdf.setFont('Helvetica', 11)
        pdf.drawCentredString(width / 2, 790, 'Jl. Mawar No. 123 Medan')
        pdf.drawCentredString(width / 2, 775, 'Telp : 0812-3456-7890')
        pdf.drawCentredString(width / 2, 760, 'Instagram : @sewabajunikah')

        pdf.line(40, 745, 555, 745)

        # TITLE STRUK
        pdf.setFont('Helvetica-Bold', 15)
        pdf.drawCentredString(width / 2, 720, 'STRUK PENYEWAAN')

        # INFORMASI TRANSAKSI
        pdf.setFont('Helvetica', 11)
        pdf.drawString(50, 690, 'Kode Transaksi')
        pdf.drawString(180, 690, f': {transaksi.kode_transaksi}')

        pdf.drawString(50, 670, 'Nama Penyewa')
        pdf.drawString(180, 670, f': {transaksi.penyewa.nama_penyewa}')

        pdf.drawString(50, 650, 'Tanggal Sewa')
        pdf.drawString(180, 650, f': {transaksi.tanggal_sewa}')

        pdf.drawString(50, 630, 'Tanggal Kembali')
        pdf.drawString(180, 630, f': {transaksi.tanggal_kembali}')

        pdf.drawString(50, 610, 'Status')
        pdf.drawString(180, 610, f': {transaksi.status_sewa}')

        pdf.line(40, 590, 555, 590)

        # HEADER TABEL
        pdf.setFont('Helvetica-Bold', 11)
        pdf.drawString(50, 570, 'Nama Baju')
        pdf.drawString(300, 570, 'Qty')
        pdf.drawString(360, 570, 'Harga')
        pdf.drawString(470, 570, 'Subtotal')

        pdf.line(40, 560, 555, 560)

        # DETAIL ITEM
        y = 535
        pdf.setFont('Helvetica', 10)

        for detail in transaksi.detail_transaksi.all():
            pdf.drawString(50, y, str(detail.baju.nama_baju))
            pdf.drawString(310, y, str(detail.qty))
            pdf.drawString(360, y, f'Rp {detail.harga_sewa}')
            pdf.drawString(470, y, f'Rp {detail.subtotal}')
            y -= 25

        # GARIS TOTAL
        pdf.line(40, y, 555, y)

        # TOTAL PEMBAYARAN
        y -= 30
        pdf.setFont('Helvetica-Bold', 13)
        pdf.drawRightString(450, y, 'TOTAL')
        pdf.drawRightString(540, y, f'Rp {transaksi.total_bayar}')

        # FOOTER
        y -= 60
        pdf.setFont('Helvetica-Oblique', 11)
        pdf.drawCentredString(width / 2, y, 'Terima kasih telah menggunakan layanan kami')
        pdf.drawCentredString(width / 2, y - 18, 'Semoga acara pernikahan anda berjalan lancar')

        # TANDA TANGAN
        y -= 80
        pdf.setFont('Helvetica', 11)
        pdf.drawString(400, y, 'Hormat Kami')
        pdf.drawString(400, y - 60, 'Admin / Kasir')

        # SAVE PDF
        pdf.showPage()
        pdf.save()

        pdf_url = request.build_absolute_uri(
            settings.MEDIA_URL + 'struk/' + file_name
        )

        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Struk berhasil dibuat',
            'data': {
                'kode_transaksi': transaksi.kode_transaksi,
                'url_struk': pdf_url
            }
        }, status=status.HTTP_200_OK)