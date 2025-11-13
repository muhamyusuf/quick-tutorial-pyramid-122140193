# Analisis 19 - Databases Using SQLAlchemy

Inti langkah:
- Menambah `sqlalchemy`, `pyramid_tm`, dan `zope.sqlalchemy` agar ORM-nya terhubung dengan transaction manager Pyramid.
- `development.ini` sekarang menyertakan `sqlalchemy.url` (SQLite) plus include `pyramid_tm`.
- Dibuat modul `models.py` untuk deklarasi `Page`, `DBSession`, dan Base; ada juga script konsol `initialize_tutorial_db`.
- View wiki kini melakukan query/commit lewat DBSession, bukan dictionary in-memory.
- Test menyiapkan SQLite in-memory dengan helper `_initTestingDB()` serta functional test memakai `pyramid.paster.get_app`.

Catatan saya:
- Integrasi transaksi otomatis bikin kode view lebih bersih karena commit/rollback ditangani middleware.
- Console script wajib dijalankan sebelum aplikasi dipakai agar tabel + data awal tercipta.

