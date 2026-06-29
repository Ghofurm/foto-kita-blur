# 📋 Issue: Peningkatan UX — Transisi Blur Halus & Hapus Teks

## Ringkasan

Saat ini aplikasi sudah berfungsi dengan baik untuk mendeteksi gestur peace sign (✌️) dan memberikan efek blur. Namun, ada dua area yang perlu diperbaiki agar pengalaman pengguna lebih nyaman:

1. **Teks Indikator**: Tulisan "Peace Detected!" di layar terasa mengganggu. Kita ingin tampilan bersih, hanya fokus pada efek blurnya saja.
2. **Deteksi Terlalu Sensitif (Berkedip/Flicker)**: Saat ini, jika tangan bergerak sedikit saja atau sistem gagal mendeteksi gestur selama 1 frame, efek blur langsung hilang dan berkedip. Kita ingin agar efek blur bisa lebih stabil (bertahan sesaat meski deteksi sempat hilang) agar perpindahannya lebih smooth.

---

## 🎯 Goal

- Menghapus tulisan "Peace Detected!" dari layar.
- Menambahkan penundaan (delay/cooldown) pada hilangnya efek blur, sehingga jika tangan bergerak sedikit, blur tidak langsung hilang.

---

## 📝 Instruksi Implementasi

Kamu hanya perlu mengubah file utama aplikasi. Kerjakan langkah-langkah berikut:

### Step 1: Hapus Teks Status
**File:** `src/main.py`
- Cari bagian kode yang mengaplikasikan efek ke frame (di dalam loop kamera).
- **Hapus** baris kode yang memanggil fungsi `add_status_text`.
- (Opsional) Hapus juga import `add_status_text` di bagian paling atas file agar rapi.

### Step 2: Buat Blur Lebih Smooth (Tambah Delay)
**File:** `src/main.py`
Untuk mencegah blur yang berkedip, kita akan menggunakan bantuan waktu untuk menahan efek blur.

**Panduan Logika:**
1. Tambahkan `import time` di bagian atas file.
2. Sebelum masuk ke loop kamera (`while True:`), buat variabel untuk mencatat kapan terakhir kali peace sign terdeteksi. Contoh: `waktu_terakhir_deteksi = 0`
3. Tentukan durasi delay, misalnya 1 atau 1.5 detik.
4. Di dalam loop kamera, perbarui logika blurnya menjadi seperti ini:
   - Jika detektor menemukan gestur *peace sign* di frame saat ini, perbarui `waktu_terakhir_deteksi` dengan waktu sekarang (menggunakan `time.time()`).
   - Cek kondisi untuk memberikan efek blur: 
     - Apakah gestur terdeteksi di frame ini? **ATAU**
     - Apakah selisih antara waktu sekarang dan `waktu_terakhir_deteksi` masih di bawah batas durasi delay?
   - Jika salah satu kondisi di atas benar, aplikasikan fungsi `apply_blur` pada frame.

### Step 3: Verifikasi
Jalankan aplikasi kembali untuk melakukan pengetesan:

```bash
source .venv/bin/activate
python3 src/main.py
```

Pastikan hal berikut terjadi:
- Saat menunjukkan peace sign, kamera langsung menjadi blur.
- **Tidak ada** tulisan apapun di layar.
- Ketika kamu menurunkan tangan atau gestur berubah, efek blur **tidak langsung hilang**, melainkan menunggu sekitar 1 detik sebelum layar kembali normal.

---

## ⚠️ Catatan
- Gunakan bahasa yang mudah dipahami dalam menulis kode (tidak perlu algoritma rumit, cukup pakai `time.time()`).
- File modul lain seperti `src/detector.py` atau `src/effects.py` tidak perlu diubah, cukup modifikasi logika di `src/main.py`.
