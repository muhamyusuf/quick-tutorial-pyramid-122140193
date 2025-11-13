# Analisis 16 - Collecting Application Info With Logging

Inti langkah:
- View menambahkan logger (`logging.getLogger(__name__)`) lalu mencatat pesan `DEBUG` setiap kali dipanggil.
- `development.ini` dikonfigurasi ulang untuk mendefinisikan logger `tutorial`, handler console, serta formatter generik.
- Setelah run, pesan akan muncul di terminal dan juga di panel debugtoolbar jika aktif.

Catatan saya:
- Pakai nama logger modul bikin filtering gampang saat aplikasi makin besar.
- Konfigurasi logging via `.ini` memudahkan deploy karena level/handler bisa diubah tanpa edit kode.

