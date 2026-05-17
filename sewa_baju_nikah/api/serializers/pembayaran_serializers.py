from rest_framework import serializers
from django.contrib.auth.models import User

from sewa_baju_nikah_app.models import  Pembayaran


class PembayaranSerializer(serializers.ModelSerializer):

    kode_transaksi = serializers.CharField(
        source='transaksi.kode_transaksi',
        read_only=True
    )

    class Meta:
        model = Pembayaran
        fields = '__all__'