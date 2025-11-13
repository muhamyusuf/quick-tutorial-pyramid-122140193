# Analisis 4 - Easier Development with debugtoolbar

Inti langkah:
- Tambahin `pyramid_debugtoolbar` sebagai extras `[dev]`, dipasang via `pip install -e ".[dev]"`.
- `development.ini` diberi `pyramid.includes = pyramid_debugtoolbar` supaya add-on otomatis di-hook ke app.
- Toolbar nyuntik HTML ke akhir body sehingga bisa akses panel debugging, request history, dan traceback yang enak dibaca.

Catatan saya:
- Kalau tiba-tiba layout rusak, cukup comment baris include sementara; nggak perlu cabut paketnya.
- Extras `[dev]` menjaga dependency debug nggak ikut ke produksi, tinggal instal tanpa flag itu di environment rilis.

