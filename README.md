
# SISTEM INFORMASI SEWA BAJU NIKAH TRADISIONAL

fokusnya:
* katalog baju
* penyewaan
* pembayaran cash
* pengembalian
* struk

# HYBRID APP

artinya:
ada:
* USER (lihat-lihat katalog)
* KASIR/ADMIN (kelola transaksi)


# ROLE DALAM SISTEM

## 1. USER

HANYA:

* melihat katalog baju
* lihat foto
* lihat ukuran
* lihat harga
* lihat status tersedia
* lihat detail baju

TAPI:
- tidak bisa transaksi langsung
- tidak bayar online
- tidak checkout

Karena pembayaran cash.

---

# 2. KASIR

Yang melakukan:

* input penyewa
* membuat transaksi
* pembayaran cash
* cetak struk
* pengembalian baju

---

# 3. ADMIN

Mengelola:

* kategori
* ukuran
* baju
* user
* laporan

---

# FLOW USER (END USER)

---

## STEP 1 — USER BUKA APP

User membuka Flutter app.
Melihat:
* daftar baju adat
* kategori
* ukuran
* harga
* foto

---

# STEP 2 — USER TERTARIK

Misal:
user suka:

```text id="jlwm167"
Baju Adat Jawa Premium
```
---
# STEP 3 — USER DATANG KE TOKO / CHAT ADMIN

Karena pembayaran cash.
Jadi:
user:
* datang langsung
  ATAU
* chat WhatsApp admin

---

# STEP 4 — KASIR INPUT PENYEWA

Kasir login.
Lalu input:
* nama penyewa
* no hp
* alamat

---
# STEP 5 — KASIR BUAT TRANSAKSI

Kasir pilih:
* baju
* tanggal sewa
* tanggal kembali
---
# STEP 6 — SISTEM CEK STOK

Kalau:

```text id="-vesm6"
stok > 0
```

boleh transaksi.

---

# STEP 7 — STOK BERKURANG

Misal:
stok awal:

```text id="jlwm168"
2
```

setelah disewa:

```text id="jlwm169"
1
```

Kalau:

```text id="jlwm170"
0
```

maka:

```text id="jlwm171"
status_ketersediaan = TIDAK_TERSEDIA
```

---

# STEP 8 — PEMBAYARAN CASH

Kasir menerima uang cash.

Lalu:
buat data pembayaran.

---

# STEP 9 — CETAK STRUK

Output:

* kode transaksi
* nama penyewa
* nama baju
* tanggal sewa
* total bayar

---

# STEP 10 — PENGEMBALIAN

Saat baju kembali:

Kasir klik:

# KEMBALIKAN BAJU

---

# STEP 11 — STOK BERTAMBAH

Misal:

```text id="jlwm172"
stok = 0
```

jadi:

```text id="jlwm173"
stok = 1
```

lalu:

```text id="jlwm174"
status_ketersediaan = TERSEDIA
```

---

# KESIMPULAN FLOW

# USER

hanya:
- lihat katalog
- lihat ukuran
- lihat harga
- lihat status tersedia

---

# KASIR

yang melakukan:
- transaksi
- pembayaran cash
- pengembalian
- cetak struk

---

# PUBLIC API

tanpa login:

```text id="jlwm175"
GET /baju-nikah/
GET /kategori/
GET /ukuran/
GET /detail-baju/
```

untuk Flutter katalog.

---

# PRIVATE API

login kasir/admin:

```text id="jlwm176"
POST /penyewa/
POST /transaksi/
POST /pembayaran/
POST /pengembalian/
```
