from rest_framework import serializers
from django.contrib.auth.models import User

from sewa_baju_nikah_app.models import  DetailTransaksiSewa, TransaksiSewa


class DetailTransaksiSewaSerializer(serializers.ModelSerializer):

    nama_baju = serializers.CharField(
        source='baju.nama_baju',
        read_only=True
    )

    class Meta:
        model = DetailTransaksiSewa
        fields = '__all__'


# =========================================================
# TRANSAKSI SEWA
# =========================================================

class TransaksiSewaSerializer(serializers.ModelSerializer):

    detail_transaksi = DetailTransaksiSewaSerializer(
        many=True,
        read_only=True
    )

    nama_penyewa = serializers.CharField(
        source='penyewa.nama_penyewa',
        read_only=True
    )

    class Meta:
        model = TransaksiSewa
        fields = '__all__'
