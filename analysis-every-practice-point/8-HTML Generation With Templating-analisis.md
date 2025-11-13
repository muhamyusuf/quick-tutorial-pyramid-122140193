# Analisis 8 - HTML Generation With Templating

Inti langkah:
- `pyramid_chameleon` di-include lalu setiap view memakai renderer `home.pt`.
- View kini cukup return dictionary data; HTML digarap oleh template Chameleon.
- `development.ini` mengaktifkan `pyramid.reload_templates = true` supaya perubahan template kebaca tanpa restart.
- Test unit fokus ke data yang dikembalikan, sedangkan functional test memastikan HTML akhir memuat teks sesuai.

Catatan saya:
- Berbagi template antar view jadi gampang: cukup reuse renderer yang sama tanpa duplikasi markup.
- Memisahkan data vs tampilan bikin refactor ke renderer lain (mis. JSON) tinggal ubah dekoratornya saja.

