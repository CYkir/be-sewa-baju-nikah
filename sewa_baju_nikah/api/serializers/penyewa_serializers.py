from rest_framework import serializers
from django.contrib.auth.models import User

from sewa_baju_nikah_app.models import  Penyewa

class PenyewaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Penyewa
        fields = '__all__'