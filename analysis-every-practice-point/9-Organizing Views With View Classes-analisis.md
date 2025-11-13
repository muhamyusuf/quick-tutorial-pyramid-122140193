# Analisis 9 - Organizing Views With View Classes

Inti langkah:
- View class `TutorialViews` dibuat dengan `@view_defaults(renderer='home.pt')` supaya renderer diset sekali.
- Metode `home` dan `hello` menjadi anggota kelas, memanfaatkan `self.request`.
- Unit test diperbarui dengan instansiasi kelas terlebih dahulu sebelum memanggil metode view.

Catatan saya:
- View class mempermudah berbagi state/helper antar metode, cocok buat resource yang berhubungan.
- Kita bisa override konfigurasi per metode (mis. renderer, permission) tanpa kehilangan default yang sudah di-set di kelas.

