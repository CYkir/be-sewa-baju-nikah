from rest_framework import serializers

from sewa_baju_nikah_app.models import (
    BajuNikah,
    KategoriBaju,
    UkuranBaju
)

class BajuNikahSerializer(serializers.ModelSerializer):

    # OUTPUT
    kategori = serializers.CharField(
        source='kategori.nama_kategori',
        read_only=True
    )

    ukuran = serializers.CharField(
        source='ukuran.ukuran',
        read_only=True
    )

    # INPUT FK
    kategori_id = serializers.PrimaryKeyRelatedField(
        queryset=KategoriBaju.objects.all(),
        source='kategori',
        write_only=True
    )

    ukuran_id = serializers.PrimaryKeyRelatedField(
        queryset=UkuranBaju.objects.all(),
        source='ukuran',
        write_only=True
    )

    class Meta:
        model = BajuNikah

        fields = [
            'id',
            'kategori',
            'kategori_id',
            'ukuran',
            'ukuran_id',
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