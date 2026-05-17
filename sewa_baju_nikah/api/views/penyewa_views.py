from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated
)

from sewa_baju_nikah_app.models import (
    Penyewa
)

from api.serializers.penyewa_serializers import (
    PenyewaSerializer
)

from api.permissions.role_permissions import (
    IsAdminOrKasirPermission
)





# =========================================================
# LIST & CREATE
# =========================================================

class PenyewaAPIView(APIView):


    def get_permissions(self):

        return [
            IsAuthenticated(),
            IsAdminOrKasirPermission()
        ]

    def get(self, request):

        penyewa = Penyewa.objects.filter(
            status_data='AKTIF'
        ).order_by('-id')

        serializer = PenyewaSerializer(
            penyewa,
            many=True
        )

        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Data penyewa berhasil diambil',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PenyewaSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'message': 'Penyewa berhasil ditambahkan',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Penyewa gagal ditambahkan',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

class DetailPenyewaAPIView(APIView):

    def get_permissions(self):
        return [
            IsAuthenticated(),
            IsAdminOrKasirPermission()
        ]

    def get_object(self, pk):

        try:
            return Penyewa.objects.get(
                pk=pk,
                status_data='AKTIF'
            )
        except Penyewa.DoesNotExist:
            return None

    def get(self, request, pk):
        penyewa = self.get_object(pk)
        if penyewa is None:

            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Penyewa tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = PenyewaSerializer(
            penyewa
        )

        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Detail penyewa berhasil diambil',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)


    def patch(self, request, pk):

        penyewa = self.get_object(pk)
        if penyewa is None:
            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Penyewa tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = PenyewaSerializer(
            penyewa,
            data=request.data,
            partial = True
        )

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Penyewa berhasil diupdate',
                'data': serializer.data,
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Penyewa gagal diupdate',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        penyewa = self.get_object(pk)
        if penyewa is None:
            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Penyewa tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)
        penyewa.status_data = 'NONAKTIF'
        penyewa.save()
        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Penyewa berhasil dihapus',
        }, status=status.HTTP_200_OK)