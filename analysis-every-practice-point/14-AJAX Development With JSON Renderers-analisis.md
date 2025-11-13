# Analisis 14 - AJAX Development dengan JSON Renderer

Inti langkah:
- Route baru `/howdy.json` ditambahkan lalu view `hello` diberi dua dekorator `@view_config`: satu HTML, satu JSON.
- JSON renderer built-in akan meng-serialize dictionary view menjadi `application/json` otomatis.
- Functional test memastikan konten JSON dan header `Content-Type` sesuai.

Catatan saya:
- Pendekatan multi-dekorator ini efektif buat API kecil tanpa perlu bikin view terpisah.
- Bisa juga pakai predicate `accept` untuk negosiasi konten berdasarkan header bila ingin satu route tanpa ekstensi `.json`.

