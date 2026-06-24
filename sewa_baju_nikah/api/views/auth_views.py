from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework import status

from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from sewa_baju_nikah_app.models import (
    Profile
)

from api.serializers.auth_serializers import (
    RegisterSerializer,
    LoginSerializer,
)
# REGISTER
class RegisterAPIView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data
        )
        if serializer.is_valid():
            user = serializer.save()
            profile = Profile.objects.get(
                user=user
            )

            return JsonResponse({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'message': 'Register berhasil',
                'data': {
                    'status' : 200,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': profile.role,
                        'nama_lengkap': profile.nama_lengkap,
                    }
                }
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({

            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Register gagal',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

# LOGIN
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(
            data=request.data
        )
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(
                user=user
            )
            profile = Profile.objects.get(
                user=user
            )

            return JsonResponse({

                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Login berhasil',
                'data': {
                    'token': token.key,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': profile.role,
                        'nama_lengkap': profile.nama_lengkap,
                    }
                }
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Login gagal',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

# LOGOUT
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        request.user.auth_token.delete()
        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Logout berhasil',
        }, status=status.HTTP_200_OK)