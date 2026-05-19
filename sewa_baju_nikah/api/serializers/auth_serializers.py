from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from sewa_baju_nikah_app.models import  Profile


# =========================================================
# REGISTER
# =========================================================

class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
        ]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )

        Profile.objects.create(
            user=user,
            role='USER',
            nama_lengkap=f"{user.first_name} {user.last_name}",
            alamat='-',
            no_hp='-',
            jenis_kelamin='L'
        )

        return user

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            username=username,
            password=password
        )

        if not user:

            raise serializers.ValidationError(
                'Username atau password salah'
            )

        attrs['user'] = user

        return attrs
