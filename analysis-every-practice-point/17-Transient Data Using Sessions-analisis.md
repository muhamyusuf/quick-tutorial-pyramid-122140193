# Analisis 17 - Transient Data Using Sessions

Inti langkah:
- Mengaktifkan session bawaan Pyramid dengan `SignedCookieSessionFactory('itsaseekreet')` lalu dipasang saat membuat Configurator.
- View class menambah properti `counter` yang menyimpan angka di `request.session` dan dipakai di template.
- Nilai counter bertahan lintas request maupun restart server selama cookie masih valid.

Catatan saya:
- Signed cookie cocok buat demo/fitur ringan; untuk data besar atau rahasia harus ganti backend (Redis, DB).
- Property pada view class memudahkan akses state session tanpa mengulang kode di tiap metode.

