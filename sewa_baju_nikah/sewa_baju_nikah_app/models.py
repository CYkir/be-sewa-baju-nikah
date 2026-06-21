from django.db import models
from django.contrib.auth.models import User
import os
import time

# =========================================================
# ABSTRACT MODEL
# =========================================================

class StatusModel(models.Model):

    STATUS_DATA = (
        ('AKTIF', 'AKTIF'),
        ('NONAKTIF', 'NONAKTIF'),
    )

    status_data = models.CharField(
        max_length=20,
        choices=STATUS_DATA,
        default='AKTIF'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True

    # =====================================================
    # SOFT DELETE
    # =====================================================

    def delete(self, *args, **kwargs):
        self.status_data = 'NONAKTIF'
        self.save()


# =========================================================
# PROFILE
# =========================================================

class Profile(StatusModel):

    ROLE_CHOICES = (
        ('ADMIN', 'ADMINISTRATOR'),
        ('KASIR', 'KASIR'),
        ('USER', 'USER'),
    )

    JENIS_KELAMIN = (
        ('L', 'Laki-Laki'),
        ('P', 'Perempuan'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='USER'
    )

    nama_lengkap = models.CharField(
        max_length=100
    )

    alamat = models.TextField()

    no_hp = models.CharField(
        max_length=20
    )

    jenis_kelamin = models.CharField(
        max_length=2,
        choices=JENIS_KELAMIN
    )

    foto_profile = models.ImageField(
        upload_to='profile/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nama_lengkap


# =========================================================
# KATEGORI BAJU
# =========================================================

class KategoriBaju(StatusModel):

    nama_kategori = models.CharField(
        max_length=100
    )

    asal_daerah = models.CharField(
        max_length=100
    )

    deskripsi = models.TextField()

    harga_dasar = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return self.nama_kategori


# =========================================================
# UKURAN BAJU
# =========================================================

class UkuranBaju(StatusModel):

    ukuran = models.CharField(
        max_length=10
    )
    lingkar_dada = models.FloatField()
    panjang_baju = models.FloatField()
    rekomendasi_berat_badan = models.FloatField()
    rekomendasi_tinggi_badan = models.FloatField()
    keterangan = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.ukuran


# =========================================================
# BAJU NIKAH
# =========================================================

def upload_foto_baju(instance, filename):
    timestamp = int(time.time())
    extension = filename.split('.')[-1]
    nama_baju = instance.nama_baju.replace(' ', '_')
    kategori = instance.kategori.nama_kategori.replace(' ', '_')
    ukuran = instance.ukuran.ukuran.replace(' ', '_')
    filename = f"{nama_baju}_{kategori}_{ukuran}_{timestamp}.{extension}"

    return os.path.join(
        'baju/',
        filename
    )

class BajuNikah(StatusModel):

    KONDISI_CHOICES = (
        ('BAIK', 'BAIK'),
        ('CUKUP', 'CUKUP'),
        ('RUSAK', 'RUSAK'),
    )

    STATUS_TERSEDIA = (
        ('TERSEDIA', 'TERSEDIA'),
        ('TIDAK_TERSEDIA', 'TIDAK_TERSEDIA'),
    )
    kategori = models.ForeignKey(
        KategoriBaju,
        on_delete=models.CASCADE
    )
    ukuran = models.ForeignKey(
        UkuranBaju,
        on_delete=models.CASCADE
    )
    nama_baju = models.CharField(
        max_length=100
    )
    warna = models.CharField(
        max_length=50
    )
    stok = models.PositiveIntegerField(
        default=1
    )
    harga_sewa = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    kondisi = models.CharField(
        max_length=20,
        choices=KONDISI_CHOICES,
        default='BAIK'
    )
    status_ketersediaan = models.CharField(
        max_length=30,
        choices=STATUS_TERSEDIA,
        default='TERSEDIA'
    )
    deskripsi = models.TextField()
    foto_baju = models.ImageField(
        upload_to=upload_foto_baju,
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        try:
            old_data = BajuNikah.objects.get(id=self.id)
            # HAPUS FOTO LAMA
            if old_data.foto_baju != self.foto_baju:
                if old_data.foto_baju:
                    if os.path.isfile(
                        old_data.foto_baju.path
                    ):
                        os.remove(
                            old_data.foto_baju.path
                        )
        except:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nama_baju} - {self.ukuran}"
# =========================================================
# PENYEWA
# =========================================================

class Penyewa(StatusModel):

    JENIS_KELAMIN = (
        ('L', 'Laki-Laki'),
        ('P', 'Perempuan'),
    )

    nama_penyewa = models.CharField(
        max_length=100
    )

    nik = models.CharField(
        max_length=30,
        unique=True
    )

    alamat = models.TextField()

    no_hp = models.CharField(
        max_length=20
    )

    jenis_kelamin = models.CharField(
        max_length=2,
        choices=JENIS_KELAMIN
    )

    tanggal_daftar = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nama_penyewa

# =========================================================
# TRANSAKSI SEWA
# =========================================================

class TransaksiSewa(StatusModel):

    STATUS_SEWA = (
        ('DIPROSES', 'DIPROSES'),
        ('DISEWA', 'DISEWA'),
        ('DIKEMBALIKAN', 'DIKEMBALIKAN'),
        ('SELESAI', 'SELESAI'),
        ('DIBATALKAN', 'DIBATALKAN'),
    )

    kode_transaksi = models.CharField(
        max_length=50,
        unique=True
    )

    penyewa = models.ForeignKey(
        Penyewa,
        on_delete=models.CASCADE
    )

    tanggal_sewa = models.DateField()

    tanggal_kembali = models.DateField()
    lama_sewa = models.PositiveIntegerField()

    total_bayar = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    tanggal_dikembalikan = models.DateField(
    null=True,
    blank=True
)

    status_sewa = models.CharField(
        max_length=30,
        choices=STATUS_SEWA,
        default='DIPROSES'
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    catatan = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.kode_transaksi

# =========================================================
# DETAIL TRANSAKSI SEWA
# =========================================================

class DetailTransaksiSewa(StatusModel):

    transaksi = models.ForeignKey(
        TransaksiSewa,
        on_delete=models.CASCADE,
        related_name='detail_transaksi'
    )

    baju = models.ForeignKey(
        BajuNikah,
        on_delete=models.CASCADE
    )

    qty = models.PositiveIntegerField(
        default=1
    )

    harga_sewa = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.transaksi.kode_transaksi}"

# =========================================================
# PEMBAYARAN
# =========================================================

class Pembayaran(StatusModel):

    transaksi = models.OneToOneField(
        TransaksiSewa,
        on_delete=models.CASCADE
    )

    tanggal_bayar = models.DateTimeField(
        auto_now_add=True
    )

    total_bayar = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    diterima_oleh = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    keterangan = models.TextField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.transaksi.kode_transaksi