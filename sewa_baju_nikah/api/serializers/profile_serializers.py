from rest_framework import serializers
from django.contrib.auth.models import User

from sewa_baju_nikah_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source='user.username',
        read_only=True
    )

    email = serializers.CharField(
        source='user.email',
        read_only=True
    )

    jenis_kelamin_label = serializers.CharField(
        source='get_jenis_kelamin_display',
        read_only=True
    )

    foto_profile_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'username',
            'email',
            'role',
            'nama_lengkap',
            'alamat',
            'no_hp',
            'jenis_kelamin',
            'jenis_kelamin_label',
            'foto_profile',
            'foto_profile_url',
            'status_data',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'user',
            'username',
            'email',
            'role',
            'status_data',
            'created_at',
            'updated_at',
        ]

    def get_foto_profile_url(self, obj):
        request = self.context.get('request')

        if obj.foto_profile:
            if request:
                return request.build_absolute_uri(
                    obj.foto_profile.url
                )

            return obj.foto_profile.url

        return None