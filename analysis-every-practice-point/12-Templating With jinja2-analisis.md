# Analisis 12 - Templating With Jinja2

Inti langkah:
- Tambah `pyramid_jinja2` ke dependensi lalu include di configurator.
- Renderer view diganti ke `home.jinja2`, template memakai sintaks `{{ }}` ala Jinja.
- Selain perubahan renderer, alur kode tetap sama dengan versi Chameleon sehingga gampang tukar mesin templating.

Catatan saya:
- Ini bukti kalau Pyramid agnostik soal templating; cukup daftarkan renderer baru dan rename file template.
- Jika proyek punya mix template engine, keduanya bisa coexist selama renderer-nya di-declare pada masing-masing view.

