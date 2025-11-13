# Analisis 11 - Dispatching URLs To Views With Routing

Inti langkah:
- Route `/howdy/{first}/{last}` memperkenalkan pattern substitusi dan aksesnya lewat `request.matchdict`.
- Template menampilkan nilai parameter yang diambil dari URL, sedangkan test functional ngecek nama muncul di body.
- View class tetap digunakan tapi sekarang data bergantung pada segmen URL.

Catatan saya:
- Urutan route penting; Pyramid eksplisit supaya kita kontrol prioritas tanpa tebak-tebakan framework.
- `matchdict` tersedia di banyak hook (view, tween, dll.) jadi aman untuk dipakai lintas lapisan.

