from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from sewa_baju_nikah_app.models import Profile
from api.serializers.profile_serializers import ProfileSerializer
class ProfileAPIView(APIView):
    permission_classes = [
        IsAuthenticated
    ]
    def get(self, request):
        try:
            profile = Profile.objects.get(
                user=request.user,
                status_data='AKTIF'
            )
        except Profile.DoesNotExist:
            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Profile tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(
            profile,
            context={
                'request': request
            }
        )
        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Profile berhasil diambil',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)