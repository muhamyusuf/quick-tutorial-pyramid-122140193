# Analisis 2 - Python Packages for Pyramid Applications

Inti langkah:
- Workspace tiap step dijadikan proyek Python penuh dengan `setup.py` dan paket `tutorial`.
- `pip install -e .` nge-link proyek secara editable, jadi setiap perubahan langsung kebaca tanpa reinstall.
- View dan konfigurasi masih ditempatkan di modul terpisah (`tutorial/app.py`), tapi sudah berada di dalam paket bernama jelas.
- Eksekusi aplikasi tetap manual `python tutorial/app.py`, cuma sekarang berasal dari paket.

Catatan saya:
- Struktur ini ngasih pondasi buat dependensi antar step, juga menyiapkan tempat buat modul tambahan nantinya.
- Walau menjalankan modul dalam paket bukan pola produksi, latihan ini penting supaya ngerti kenapa nanti `pserve` butuh entry point.

