# Analisis 0 - Requirements

Inti langkah:
- Gunakan Python 3.8 plus virtual environment `venv` supaya dependensi Pyramid nggak bentrok dengan sistem global.
- Struktur kerja yang dianjurkan adalah `workspace -> project -> package`, jadi kita gampang mindahin setiap step tutorial tanpa bikin folder berantakan.
- Variabel lingkungan `VENV` dipakai buat nyimpen path virtualenv agar perintah pip/python lebih singkat, terutama saat gonta-ganti OS.
- Setelah bikin virtualenv, langsung upgrade pip dan setuptools sebelum install Pyramid 2.0.2 + Waitress biar toolchain terbaru.

Catatan saya:
- Semua instruksi pakai gaya Unix, jadi user Windows mesti konversi manual; lebih aman kalau kita siapin alias/perintah PowerShell di dok pribadi.
- Step ini belum ada kode, tapi wajib selesai sebelum praktik berikutnya supaya `pserve`, `pytest`, sampai add-on lain jalan mulus.

