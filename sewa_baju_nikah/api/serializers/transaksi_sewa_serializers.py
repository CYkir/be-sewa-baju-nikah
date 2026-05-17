from rest_framework import serializers

from sewa_baju_nikah_app.models import (
    TransaksiSewa,
    DetailTransaksiSewa,
    BajuNikah
)

class DetailTransaksiSewaSerializer(serializers.ModelSerializer):
    nama_baju = serializers.CharField(
        source='baju.nama_baju',
        read_only=True
    )
    foto_baju = serializers.ImageField(
        source='baju.foto_baju',
        read_only=True
    )
    class Meta:
        model = DetailTransaksiSewa
        fields = [
            'id',
            'baju',
            'nama_baju',
            'foto_baju',
            'qty',
            'harga_sewa',
            'subtotal',
        ]

class TransaksiSewaSerializer(serializers.ModelSerializer):
    detail_transaksi = DetailTransaksiSewaSerializer(
        many=True
    )
    nama_penyewa = serializers.CharField(
        source='penyewa.nama_penyewa',
        read_only=True
    )
    class Meta:
        model = TransaksiSewa
        fields = [
            'id',
            'kode_transaksi',
            'penyewa',
            'nama_penyewa',
            'tanggal_sewa',
            'tanggal_kembali',
            'tanggal_dikembalikan',
            'lama_sewa',
            'total_bayar',
            'status_sewa',
            'catatan',
            'detail_transaksi',
            'status_data',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        detail_data = validated_data.pop(
            'detail_transaksi'
        )
        transaksi = TransaksiSewa.objects.create(
            **validated_data
        )
        total_bayar = 0
        for item in detail_data:
            baju = item['baju']
            qty = item['qty']
            harga = baju.harga_sewa
            subtotal = harga * qty
            # CREATE DETAIL
            DetailTransaksiSewa.objects.create(
                transaksi=transaksi,
                baju=baju,
                qty=qty,
                harga_sewa=harga,
                subtotal=subtotal
            )

            # UPDATE STOK
            baju.stok -= qty

            # STATUS TERSEDIA
            if baju.stok <= 0:

                baju.status_ketersediaan = (
                    'TIDAK_TERSEDIA'
                )
            baju.save()
            total_bayar += subtotal
        transaksi.total_bayar = total_bayar
        transaksi.save()
        return transaksi