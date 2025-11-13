# Analisis 20 - Logins with Authentication

Inti langkah:
- Tambah `bcrypt` untuk hashing password dan buat modul `security.py` berisi helper `hash_password`, `check_password`, serta `SecurityPolicy`.
- `development.ini` menyimpan `tutorial.secret` yang dipakai `AuthTktCookieHelper` buat menandatangani cookie login.
- View class sekarang punya metode login/logout; login memeriksa kredensial dan memanggil `remember`, logout memakai `forget`.
- Template homepage menampilkan tautan login/logout sesuai status `request.authenticated_userid`.

Catatan saya:
- Simpan hash password (bukan plaintext) sekalipun contoh kecil, supaya gampang upgrade ke backend user sungguhan.
- `came_from` menjaga UX: setelah login sukses user balik ke halaman yang sebelumnya diminta.

