# Analisis 21 - Protecting Resources With Authorization

Inti langkah:
- Root factory (`authorization.resources.Root`) mendefinisikan ACL: semua orang boleh `view`, grup `group:editors` boleh `edit`.
- `SecurityPolicy` sekarang punya daftar `GROUPS`, metode `effective_principals`, dan `permits` yang memanfaatkan `ACLHelper`.
- View `hello` diberi `permission='edit'`, sementara `login` juga didaftarkan sebagai `@forbidden_view_config` supaya otomatis dipakai saat akses ditolak.
- Ketika user `viewer` mencoba `/howdy`, Pyramid mengarahkan ke login karena tidak punya permission `edit`.

Catatan saya:
- Pemisahan autentikasi dan otorisasi bikin kita bebas mengganti penyimpanan user, selama `effective_principals` dan ACL konsisten.
- Gunakan prinsip least privilege: permission didefinisikan dekat resource (Root atau child) agar mudah audit siapa boleh apa.

