from rest_framework import serializers

from sewa_baju_nikah_app.models import (
    BajuNikah,
    KategoriBaju,
    UkuranBaju
)

class BajuNikahSerializer(serializers.ModelSerializer):

    kategori = serializers.PrimaryKeyRelatedField(
        queryset=KategoriBaju.objects.all()
    )

    ukuran = serializers.PrimaryKeyRelatedField(
        queryset=UkuranBaju.objects.all()
    )

    kategori_nama = serializers.CharField(
        source='kategori.nama_kategori',
        read_only=True
    )

    ukuran_nama = serializers.CharField(
        source='ukuran.ukuran',
        read_only=True
    )

    class Meta:

        model = BajuNikah
        fields = [
            'id',
            'kategori',
            'kategori_nama',
            'ukuran',
            'ukuran_nama',
            'nama_baju',
            'warna',
            'stok',
            'harga_sewa',
            'kondisi',
            'status_ketersediaan',
            'deskripsi',
            'foto_baju',

            'status_data',
            'created_at',
            'updated_at',
        ]