from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,  AllowAny

from sewa_baju_nikah_app.models import (
    KategoriBaju
)

from api.serializers.kategori_baju_serializers import (
    KategoriBajuSerializer
)

from api.permissions.role_permissions import (
    IsAdminOrKasirPermission
)


# LIST & CREATE


class KategoriBajuAPIView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [
            IsAuthenticated(),
            IsAdminOrKasirPermission()
        ]

    # permission_classes = [
    #     IsAuthenticated,
    #     IsAdminOrKasirPermission
    # ]
    # GET ALL DATA
    def get(self, request):

        kategori = KategoriBaju.objects.filter(
            status_data='AKTIF'
        ).order_by('-id')

        serializer = KategoriBajuSerializer(
            kategori,
            many=True
        )

        return JsonResponse({

            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Data kategori berhasil diambil',
            'data': serializer.data,

        }, status=status.HTTP_200_OK)

    # CREATE DATA
    def post(self, request):

        serializer = KategoriBajuSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()
            return JsonResponse({

                'success': True,
                'status': status.HTTP_201_CREATED,
                'message': 'Kategori berhasil ditambahkan',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Kategori gagal ditambahkan',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


# DETAIL, UPDATE, DELETE
class DetailKategoriBajuAPIView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [
            IsAuthenticated(),
            IsAdminOrKasirPermission()
        ]

    # GET OBJECT
    def get_object(self, pk):
        try:
            return KategoriBaju.objects.get(
                pk=pk,
                status_data='AKTIF'
            )
        except KategoriBaju.DoesNotExist:

            return None

    # DETAIL DATA

    def get(self, request, pk):

        kategori = self.get_object(pk)

        if kategori is None:

            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Kategori tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = KategoriBajuSerializer(
            kategori
        )

        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Detail kategori berhasil diambil',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)

    # UPDATE DATA
    def patch(self, request, pk):
        kategori = self.get_object(pk)
        if kategori is None:
            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Kategori tidak ditemukan',

            }, status=status.HTTP_404_NOT_FOUND)

        serializer = KategoriBajuSerializer(
            kategori,
            data=request.data,
            partial = True
        )

        if serializer.is_valid():

            serializer.save()

            return JsonResponse({

                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Kategori berhasil diupdate',
                'data': serializer.data,
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Kategori gagal diupdate',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)


    # SOFT DELETE
    def delete(self, request, pk):
        kategori = self.get_object(pk)
        if kategori is None:
            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Kategori tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)
        kategori.status_data = 'NONAKTIF'
        kategori.save()
        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Kategori berhasil dihapus',
        }, status=status.HTTP_200_OK)