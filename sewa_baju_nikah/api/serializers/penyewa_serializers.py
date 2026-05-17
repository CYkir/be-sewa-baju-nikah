from rest_framework import serializers

from sewa_baju_nikah_app.models import (
    Penyewa
)

class PenyewaSerializer(serializers.ModelSerializer):

    class Meta:

        model = Penyewa
        fields = [
            'id',
            'nama_penyewa',
            'nik',
            'alamat',
            'no_hp',
            'jenis_kelamin',
            'tanggal_daftar',
            'status_data',
            'created_at',
            'updated_at',
        ]