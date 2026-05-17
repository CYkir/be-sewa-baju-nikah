from rest_framework import serializers

from sewa_baju_nikah_app.models import (
    UkuranBaju
)

class UkuranBajuSerializer(serializers.ModelSerializer):

    class Meta:
        model = UkuranBaju
        fields = [
            'id',
            'ukuran',
            'lingkar_dada',
            'panjang_baju',
            'rekomendasi_berat_badan',
            'rekomendasi_tinggi_badan',
            'keterangan',
            'status_data',
            'created_at',
            'updated_at',
        ]