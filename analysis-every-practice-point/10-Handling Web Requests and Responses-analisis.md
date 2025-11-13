# Analisis 10 - Handling Web Requests and Responses

Inti langkah:
- Menunjukkan penggunaan `HTTPFound` untuk redirect dan `Response` untuk kontrol header/body manual.
- View `plain` membaca query string via `request.params`/`request.GET` dan men-set `content_type` ke `text/plain`.
- Routing sederhana (`/` mengarah ke redirect, `/plain` menampilkan hasil) memperlihatkan siklus lengkap request-response.
- Tes mencakup skenario dengan dan tanpa parameter `name`.

Catatan saya:
- `request.url` berguna buat debugging karena menunjukkan URL persis termasuk parameter.
- Respons plain text berguna sebagai titik awal API/diagnostik sebelum masuk templating.

