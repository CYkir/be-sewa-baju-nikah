from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.conf.urls.static import static

from api.views.auth_views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
)

from api.views.kategori_baju_views import KategoriBajuAPIView, DetailKategoriBajuAPIView
from api.views.ukuran_baju_views import UkuranBajuAPIView, DetailUkuranBajuAPIView
from api.views.baju_nikah_views import BajuNikahAPIView, DetailBajuNikahAPIView, BajuNikahFilterApi
from api.views.penyewa_views import PenyewaAPIView, DetailPenyewaAPIView
from api.views.transaksi_sewa_views import TransaksiSewaAPIView, TransaksiSewaFilterApi
from api.views.pembayaran_views import  PembayaranAPIView
from api.views.pengembalian_views import  PengembalianAPIView
from api.views.struk_views import CetakStrukAPIView
from api.views.selesai_transaksi_views import SelesaikanTransaksiAPIView

app_name = 'api'

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(),name='register'),
    path('auth/login/',LoginAPIView.as_view(),name='login'),
    path('auth/logout/',LogoutAPIView.as_view(), name='logout'),

    #Kategori
    path('kategori-baju/',KategoriBajuAPIView.as_view(),name='kategori-baju'),
    path('kategori-baju/<int:pk>/',DetailKategoriBajuAPIView.as_view(),name='detail-kategori-baju'),

    # Ukuran Baju
    path('ukuran-baju/',UkuranBajuAPIView.as_view(),name='ukuran-baju'),
    path('ukuran-baju/<int:pk>/',DetailUkuranBajuAPIView.as_view(),name='detail-ukuran-baju'),

    # Baju Nikah
    path('baju-nikah/',BajuNikahAPIView.as_view(),name='baju-nikah'),
    path('baju-nikah/<int:pk>/',DetailBajuNikahAPIView.as_view(),name='detail-baju-nikah'),
    path('baju-nikah-filter/', BajuNikahFilterApi.as_view(), name= 'baju-nikah-filter' ),

    # Penyewa
    path('penyewa/', PenyewaAPIView.as_view(), name = 'penyewa'),
    path('penyewa/<int:pk>/' , DetailPenyewaAPIView.as_view(), name = 'detail-penyewa'),

    #Transaksi
    path('transaksi-sewa/',TransaksiSewaAPIView.as_view(),name='transaksi-sewa'),
    path('tranksaksi-sewa-filter/', TransaksiSewaFilterApi.as_view(), name='filter-transaksi'),

    #pembayaran
    path('pembayaran/', PembayaranAPIView.as_view(),name='pembayaran'),

    #Pengembalian
    path('pengembalian/<int:pk>/',PengembalianAPIView.as_view(),name='pengembalian'),

    #Selesaikan Transaksi
    path('transaksi-selesai/<int:pk>/',SelesaikanTransaksiAPIView.as_view(),name='transaksi-selesai'),

    #cetak struk
    path('struk/<int:pk>/',CetakStrukAPIView.as_view(),name='struk'),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )