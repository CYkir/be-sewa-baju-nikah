import random
from datetime import datetime

from sewa_baju_nikah_app.models import (
    DetailTransaksiSewa
)

# =========================================================
# GENERATE KODE TRANSAKSI
# =========================================================

def generate_kode_transaksi():

    random_number = random.randint(1000, 9999)

    current_date = datetime.now().strftime('%Y%m%d')

    kode = f'TRX-{current_date}-{random_number}'

    return kode

# =========================================================
# HITUNG TOTAL TRANSAKSI
# =========================================================

def hitung_total_transaksi(transaksi):

    detail = DetailTransaksiSewa.objects.filter(
        transaksi=transaksi,
        status_data='AKTIF'
    )

    total = 0

    for item in detail:

        total += item.subtotal

    return total

# =========================================================
# KURANGI STOK BAJU
# =========================================================

def kurangi_stok_baju(baju, qty):

    baju.stok -= qty

    baju.save()

# =========================================================
# TAMBAH STOK BAJU
# =========================================================

def tambah_stok_baju(baju, qty):

    baju.stok += qty

    baju.save()