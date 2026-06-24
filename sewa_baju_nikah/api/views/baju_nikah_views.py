from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework.parsers import (
    MultiPartParser,
    FormParser
)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter
)
from sewa_baju_nikah_app.models import BajuNikah
from api.serializers.baju_nikah_serializers import BajuNikahSerializer

from rest_framework import generics
from api.pagination import CustomPagination
from api.permissions.role_permissions import IsAdminOrKasirPermission
import django_filters.rest_framework

# LIST & CREATE
class BajuNikahAPIView(APIView):
    parser_classes = (
        MultiPartParser,
        FormParser
    )
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [
            IsAuthenticated(),
            IsAdminOrKasirPermission()
        ]
    def get(self, request):
        baju = BajuNikah.objects.filter(
            status_data='AKTIF'
        ).order_by('-id')
        paginator = CustomPagination()
        paginated_data = paginator.paginate_queryset(
            baju,
            request
        )
        serializer = BajuNikahSerializer(
            baju,
            many=True
        )
        return paginator.get_paginated_response(
            serializer.data
        )

    def post(self, request):
        serializer = BajuNikahSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'message': 'Baju nikah berhasil ditambahkan',
                'data': serializer.data,
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Baju nikah gagal ditambahkan',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

class DetailBajuNikahAPIView(APIView):
    parser_classes = (
        MultiPartParser,
        FormParser
    )
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [
            IsAuthenticated(),
            IsAdminOrKasirPermission()
        ]
    def get_object(self, pk):
        try:
            return BajuNikah.objects.get(
                pk=pk,
                status_data='AKTIF'
            )
        except BajuNikah.DoesNotExist:
            return None

    def get(self, request, pk):
        baju = self.get_object(pk)
        if baju is None:
            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Baju nikah tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = BajuNikahSerializer(
            baju
        )
        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Detail baju nikah berhasil diambil',
            'data': serializer.data,
        }, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        baju = self.get_object(pk)
        if baju is None:
            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Baju nikah tidak ditemukan',

            }, status=status.HTTP_404_NOT_FOUND)

        serializer = BajuNikahSerializer(
            baju,
            data=request.data,
            partial = True
        )

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Baju nikah berhasil diupdate',
                'data': serializer.data,
            }, status=status.HTTP_200_OK)
        return JsonResponse({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Baju nikah gagal diupdate',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        baju = self.get_object(pk)
        if baju is None:
            return JsonResponse({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Baju nikah tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)
        baju.status_data = 'NONAKTIF'
        baju.save()
        return JsonResponse({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Baju nikah berhasil dihapus',
        }, status=status.HTTP_200_OK)

class BajuNikahFilterApi(generics.ListAPIView):
    queryset = BajuNikah.objects.filter(
            status_data='AKTIF'
    ).order_by('-id')

    serializer_class = BajuNikahSerializer
    pagination_class = CustomPagination
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, SearchFilter,OrderingFilter,]
    filterset_fields = ['kategori__nama_kategori']
    search_fields = [
        'nama_baju',
        'kategori__nama_kategori',
        'warna',
    ]
    ordering_fields = ['created_at', 'harga_sewa',]
