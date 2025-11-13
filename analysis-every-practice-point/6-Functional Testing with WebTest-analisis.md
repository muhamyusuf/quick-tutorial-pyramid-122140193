# Analisis 6 - Functional Testing with WebTest

Inti langkah:
- `webtest` ditambah ke extras supaya bisa ngetes WSGI app end-to-end tanpa server HTTP beneran.
- Functional test bikin instance `TestApp(main({}))` lalu melakukan `get` ke route dan cek isi body.
- Tetap dipertahankan unit test lama, jadi coverage mencakup level fungsi dan level request.

Catatan saya:
- WebTest bypass jaringan sehingga cepat buat TDD, tapi tetap memproses routing, render, dan middleware.
- Penting pastikan file test nggak executable, karena `pytest` bisa skip kalau ada bit eksekusi yang bikin dia deteksi sebagai script.

