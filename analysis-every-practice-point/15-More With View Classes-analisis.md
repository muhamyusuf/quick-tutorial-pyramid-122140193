# Analisis 15 - More With View Classes

Inti langkah:
- View class sekarang punya beberapa metode untuk satu route `hello` dengan predicate berbeda (`request_method`, `request_param`).
- Properti `full_name` plus atribut `view_name` dipakai ulang oleh template sehingga logika gabungan tinggal satu tempat.
- Template form memanfaatkan `request.route_url` untuk merakit URL dinamis dan menunjukkan contoh self-posting form.

Catatan saya:
- `@view_defaults(route_name='hello')` lalu override pada metode tertentu (mis. `home`) nunjukin betapa fleksibelnya konfigurasi kelas.
- Ketika butuh banyak aksi pada resource sama (view, edit, delete), pattern ini bikin kode rapih dan mudah dites.

