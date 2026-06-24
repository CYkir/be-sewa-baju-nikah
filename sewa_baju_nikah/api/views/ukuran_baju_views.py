from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from sewa_baju_nikah_app.models import UkuranBaju
from api.serializers.ukuran_baju_serializers import  UkuranBajuSerializer
from api.permissions.role_permissions import IsAdminOrKasirPermission
class UkuranBajuAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [
            IsAuthenticated(),
            IsAdminOrKasirPermission()
        ]
    def get(self, request):
        ukuran = UkuranBaju.objects.filter(
            status_data='AKTIF'
        ).order_by('-id')
        serializer = UkuranBajuSerializer(
            ukuran,
            many=True
        )
        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Data ukuran baju berhasil diambil',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UkuranBajuSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'message': 'Ukuran baju berhasil ditambahkan',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)
        return JsonResponse({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Ukuran baju gagal ditambahkan',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)
class DetailUkuranBajuAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [
            IsAuthenticated(),
            IsAdminOrKasirPermission()
        ]
    def get_object(self, pk):
        try:
            return UkuranBaju.objects.get(
                pk=pk,
                status_data='AKTIF'
            )
        except UkuranBaju.DoesNotExist:
            return None
    def get(self, request, pk):
        ukuran = self.get_object(pk)
        if ukuran is None:
            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Ukuran baju tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = UkuranBajuSerializer(
            ukuran
        )
        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Detail ukuran baju berhasil diambil',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)
    def patch(self, request, pk):
        ukuran = self.get_object(pk)
        if ukuran is None:
            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Ukuran baju tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = UkuranBajuSerializer(
            ukuran,
            data=request.data,
            partial = True
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Ukuran baju berhasil diupdate',
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        return JsonResponse({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Ukuran baju gagal diupdate',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        ukuran = self.get_object(pk)
        if ukuran is None:
            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Ukuran baju tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)
        ukuran.status_data = 'NONAKTIF'
        ukuran.save()
        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Ukuran baju berhasil dihapus',
        }, status=status.HTTP_200_OK)