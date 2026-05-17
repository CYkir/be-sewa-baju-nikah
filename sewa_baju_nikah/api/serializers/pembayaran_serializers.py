from rest_framework import serializers

from sewa_baju_nikah_app.models import (
    Pembayaran,
    TransaksiSewa
)

class PembayaranSerializer(serializers.ModelSerializer):
    kode_transaksi = serializers.CharField(
        source='transaksi.kode_transaksi',
        read_only=True
    )
    nama_penyewa = serializers.CharField(
        source='transaksi.penyewa.nama_penyewa',
        read_only=True
    )
    class Meta:
        model = Pembayaran
        fields = [
            'id',
            'transaksi',
            'kode_transaksi',
            'nama_penyewa',
            'tanggal_bayar',
            'total_bayar',
            'keterangan',
            'status_data',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'total_bayar',
            'tanggal_bayar',
        ]

    def create(self, validated_data):
        transaksi = validated_data['transaksi']
        pembayaran = Pembayaran.objects.create(
            transaksi=transaksi,
            total_bayar=transaksi.total_bayar,
            diterima_oleh=self.context[
                'request'
            ].user,
            keterangan=validated_data.get(
                'keterangan'
            )
        )
        # UPDATE STATUS TRANSAKSI
        transaksi.status_sewa = 'SELESAI'
        transaksi.save()

        return pembayaran