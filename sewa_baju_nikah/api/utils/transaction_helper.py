from datetime import datetime

from sewa_baju_nikah_app.models import (
    TransaksiSewa
)

def generate_kode_transaksi():
    tanggal = datetime.now().strftime('%Y%m%d')
    total = TransaksiSewa.objects.count() + 1
    return f"TRX-{tanggal}-{total}"