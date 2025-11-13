# Catatan Eksekusi Project Pyramid

- 13 Nov 2025 (siang): Folder masih kosong, belum ada perintah yang dijalankan.
- 13 Nov 2025 (sore):
  - Membuat virtualenv lokal di `.venv` menggunakan `python -m venv .venv`.
  - Memperbarui toolchain dengan `.venv\Scripts\python -m pip install --upgrade pip setuptools wheel`.
  - Menginstal dependensi proyek beserta tooling dev via `.venv\Scripts\pip install -e ".[dev]"`.
  - Menjalankan pengujian `.\.venv\Scripts\pytest` dan seluruh tes lulus (4 passed) dengan peringatan eksternal dari `pkg_resources`.
- 13 Nov 2025 (sore, lanjut):
  - Menjalankan inisialisasi database: `.\.venv\Scripts\python -m tutorial.initialize_db development.ini` (sukses membuat `quick_tutorial.sqlite` dan seed page 100/101).
- 13 Nov 2025 (malam):
  - Memperbaiki template Chameleon dengan menambahkan namespace TAL agar wiki page bisa dirender tanpa error.
  - Menjalankan ulang `.\.venv\Scripts\pytest` → tetap 4 passed (warning eksternal `pkg_resources`/`paste`).
- 13 Nov 2025 (malam, lanjut):
  - Memperbaiki `wiki_page.pt` (`tal:structure` diganti `tal:content="structure ..."` sesuai sintaks ZPT).
  - Re-run `.\.venv\Scripts\pytest` → 4 passed.
