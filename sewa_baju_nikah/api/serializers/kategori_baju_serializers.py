from rest_framework import serializers

from sewa_baju_nikah_app.models import KategoriBaju

class KategoriBajuSerializer(serializers.ModelSerializer):

    class Meta:
        model = KategoriBaju
        fields = [
            'id',
            'nama_kategori',
            'asal_daerah',
            'deskripsi',
            'harga_dasar',
            'status_data',
            'created_at',
            'updated_at',
        ]

