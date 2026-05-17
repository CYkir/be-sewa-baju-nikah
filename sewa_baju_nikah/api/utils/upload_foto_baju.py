import os

from sewa_baju_nikah_app.models import BajuNikah , KategoriBaju, UkuranBaju

def upload_foto_baju(instance, filename):
    extension = filename.split('.')[-1]
    nama_baju = instance.nama_baju.replace(' ', '_')
    kategori = instance.kategori.nama_kategori.replace(' ', '_')
    ukuran = instance.ukuran.ukuran.replace(' ', '_')
    filename = f"{nama_baju}_{kategori}_{ukuran}.{extension}"

    return os.path.join(
        'baju/',
        filename
    )