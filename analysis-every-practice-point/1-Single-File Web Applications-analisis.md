# Analisis 1 - Single-File Web Applications

Inti langkah:
- Pyramid bisa diajak jadi microframework cukup dengan satu berkas `app.py`, tanpa paket atau setup.py.
- `Configurator` dipakai di dalam context manager buat nambah route dan view, kemudian `make_wsgi_app()` dipassing ke Waitress.
- View `hello_world` nerima objek request ala WebOb dan balikin `Response`, cukup buat nunjukin siklus request-respons.
- Jalankan file langsung (`python app.py`) lalu cek `http://localhost:6543/` buat verifikasi.

Catatan saya:
- Momen ini bagus buat paham alur WSGI mentahnya Pyramid sebelum layer packaging muncul.
- Logging `print('Incoming request')` sengaja dibiarkan biar kelihatan kapan view dieksekusi di terminal.

