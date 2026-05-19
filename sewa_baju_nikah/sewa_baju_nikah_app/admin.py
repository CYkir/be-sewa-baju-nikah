from django.contrib import admin


from .models import (
    Profile,
    KategoriBaju,
    UkuranBaju,
    BajuNikah,
    Penyewa,
    TransaksiSewa,
    DetailTransaksiSewa,
    Pembayaran,
)

from import_export.admin import ImportExportModelAdmin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'nama_lengkap',
        'role',
        'no_hp',
        'status_data',
    ]

@admin.register(KategoriBaju)
class KategoriBajuAdmin(ImportExportModelAdmin):

    list_display = [
        'id',
        'nama_kategori',
        'asal_daerah',
        'harga_dasar',
        'status_data',
    ]

@admin.register(UkuranBaju)
class UkuranBajuAdmin(ImportExportModelAdmin):

    list_display = [
        'id',
        'ukuran',
        'rekomendasi_tinggi_badan',
        'rekomendasi_berat_badan',
        'keterangan',
        'status_data',
    ]

@admin.register(BajuNikah)
class BajuNikahAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'nama_baju',
        'kategori',
        'ukuran',
        'stok',
        'harga_sewa',
        'status_data',
    ]

@admin.register(Penyewa)
class PenyewaAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'nama_penyewa',
        'nik',
        'no_hp',
        'status_data',
    ]


@admin.register(TransaksiSewa)
class TransaksiSewaAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'kode_transaksi',
        'penyewa',
        'tanggal_sewa',
        'tanggal_kembali',
        'total_bayar',
        'status_sewa',
    ]

@admin.register(DetailTransaksiSewa)
class DetailTransaksiSewaAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'transaksi',
        'baju',
        'qty',
        'harga_sewa',
        'subtotal',
    ]


@admin.register(Pembayaran)
class PembayaranAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'transaksi',
        'tanggal_bayar',
        'total_bayar',
    ]


