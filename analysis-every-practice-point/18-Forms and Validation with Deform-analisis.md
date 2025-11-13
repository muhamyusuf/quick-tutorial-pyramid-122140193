# Analisis 18 - Forms and Validation dengan Deform

Inti langkah:
- Dependensi `deform` membawa serta Colander untuk schema/validasi; static asset Deform dipublikasikan via `add_static_view('deform_static', 'deform:static/')`.
- Dibuat schema `WikiPage` dan form Deform yang menghasilkan HTML otomatis termasuk widget RichText.
- View `WikiViews` mengelola daftar halaman dummy, mendukung tambah/edit dengan pola self-posting form dan penggunaan `deform.ValidationFailure`.
- Template iterasi resource registry Deform untuk menyertakan CSS/JS yang dibutuhkan widget.

Catatan saya:
- Mengelola form melalui schema bikin validasi terpusat; cukup ubah schema untuk mempengaruhi seluruh UI.
- Langkah ini menyiapkan pondasi sebelum data disimpan di database sungguhan pada step berikutnya.

