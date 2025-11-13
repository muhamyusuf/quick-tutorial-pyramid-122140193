# Analisis 7 - Basic Web Handling With Views

Inti langkah:
- View dipindahkan ke modul `views.py` dan registrasinya dilakukan lewat dekorator `@view_config`.
- `config.scan('.views')` di `__init__.py` membuat Pyramid mencari dekorator secara otomatis.
- Route baru `home` dan `hello` memberi contoh multi view yang saling link.
- Tes disesuaikan agar mengimpor fungsi view dari modul baru serta menambah functional test untuk tiap URL.

Catatan saya:
- Pemisahan ini bikin file bootstrap tetap kurus sementara views bisa tumbuh tanpa bikin `__init__.py` semrawut.
- Dengan deklaratif config, kita bisa mix and match view predicate tanpa harus memanggil `add_view` terus menerus.

