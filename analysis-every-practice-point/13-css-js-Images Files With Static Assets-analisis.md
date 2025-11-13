# Analisis 13 - Static Assets (CSS/JS/Gambar)

Inti langkah:
- `config.add_static_view(name='static', path='tutorial:static')` memetakan URL `/static/*` ke folder paket.
- Template memanfaatkan `request.static_url('tutorial:static/app.css')` supaya path selalu sinkron dengan konfigurasi.
- Ditambahkan CSS sederhana dan functional test memastikan `/static/app.css` tersaji.

Catatan saya:
- Lebih aman generate URL statis lewat helper daripada hardcode, karena bisa saja nanti dipasang di subpath berbeda.
- Struktur `package:subdir` memudahkan distribusi paket Pyramid lain yang bawa asset sendiri.

