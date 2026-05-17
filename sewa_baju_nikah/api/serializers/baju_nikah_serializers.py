from rest_framework import serializers

from sewa_baju_nikah_app.models import (
    BajuNikah
)

class BajuNikahSerializer(serializers.ModelSerializer):

    kategori= serializers.CharField(
        source='kategori.nama_kategori',
        read_only=True
    )

    ukuran= serializers.CharField(
        source='ukuran.ukuran',
        read_only=True
    )

    class Meta:
        model = BajuNikah
        fields = [
            'id',
            'kategori',
            'ukuran',
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