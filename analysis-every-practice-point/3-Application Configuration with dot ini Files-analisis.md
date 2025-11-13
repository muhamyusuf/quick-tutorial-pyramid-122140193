# Analisis 3 - Application Configuration dengan .ini

Inti langkah:
- `setup.py` sekarang punya entry point `paste.app_factory` supaya Pyramid tau fungsi `main` untuk bootstrap WSGI app.
- Konfigurasi dijalankan lewat `development.ini` dan command `pserve --reload`, jadi server restart otomatis ketika file berubah.
- Bootstrap kode dipindah ke `tutorial/__init__.py`, sedangkan `.ini` ngatur juga server Waitress serta logging dasar.

Catatan saya:
- Memisahkan konfigurasi dari kode bikin deployment lintas lingkungan lebih gampang; tinggal ubah `.ini` tanpa sentuh Python.
- `--reload` wajib diaktifkan selama dev karena Pyramid belum punya auto reload built-in di luar flag ini.

