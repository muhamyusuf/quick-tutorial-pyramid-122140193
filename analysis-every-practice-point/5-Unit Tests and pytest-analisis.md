# Analisis 5 - Unit Tests and pytest

Inti langkah:
- `pytest` dimasukin ke extras dev lalu proyek dijalankan lewat `pip install -e ".[dev]"`.
- Unit test menggunakan `unittest.TestCase` plus helper `pyramid.testing` buat setup configurator dummy.
- View diimpor dalam setiap test untuk jaga isolasi, request disimulasikan dengan `DummyRequest`, lalu assert status/response.
- Tes dieksekusi via `$VENV/bin/pytest tutorial/tests.py -q` supaya output ringkas.

Catatan saya:
- Pattern setUp/tearDown penting ketika nanti kita perlu inject konfigurasi (route, renderer) sebelum view dipanggil.
- Langkah ini jadi baseline; kalau ada regress di step selanjutnya, tinggal kombinasikan dengan WebTest untuk full stack.

