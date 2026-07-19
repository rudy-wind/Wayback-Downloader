# Wayback-Downloader

Script Python untuk mengambil kembali website lama dari Internet Archive Wayback Machine dan menyimpannya menjadi struktur file website lokal.

Script ini akan:

- Mengambil seluruh daftar URL yang pernah tersimpan di Wayback Machine.
- Download halaman HTML lama.
- Download asset website seperti:
  - CSS
  - JavaScript
  - Gambar
- Membuat struktur folder sesuai URL asli.
- Mengubah link Wayback menjadi link lokal.
- Menyimpan hasil clone menjadi website statis yang bisa dibuka langsung.

---

## Fitur

✅ Clone website dari Wayback Machine  
✅ Mengambil semua halaman yang tersedia  
✅ Mendukung halaman HTML bertingkat

Contoh:

```

example.com/
example.com/about.html
example.com/faq.html
example.com/blog/post.html

```

Akan menjadi:

```

website/

├── index.html
├── about.html
├── faq.html
└── blog
└── post.html

```

✅ Download asset:

```

/css/style.css
/js/script.js
/images/logo.png

```

Menjadi:

```

website/

├── css
│   └── style.css
├── js
│   └── script.js
└── images
└── logo.png

````

✅ Menghapus URL Wayback dari HTML.

Sebelum:

```html
<a href="https://web.archive.org/web/20200101000000/example.com/about.html">
````

Sesudah:

```html
<a href="about.html">
```

---

# Persyaratan

## Python

Minimal:

```
Python 3.9+
```

Cek versi Python:

```bash
python --version
```

---

# Instalasi

Clone repository:

```bash
git clone https://github.com/rudy-wind/Wayback-Downloader.git
```

Masuk ke folder:

```bash
cd Wayback-Downloader
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Cara Menggunakan

Jalankan script:

```bash
python main.py
```

Program akan meminta domain:

```
Masukkan domain (contoh: example.com):
```

Masukkan:

```
example.com
```

Kemudian folder output:

```
Folder output (default: website):
```

Jika dikosongkan:

```
website
```

akan digunakan.

---

# Contoh Penggunaan

```
Masukkan domain (contoh: example.com): example.com

Folder output (default: website):

Mengambil daftar URL Wayback...

Total URL: 523

Downloading:
100%|████████████████| 523/523

Selesai.
```

Hasil:

```
website/

├── index.html
├── contact.html
├── faq.html
├── css
│   └── style.css
├── js
│   └── app.js
└── images
    └── logo.png
```

---

# Struktur Project

```
Wayback-Downloader/

│
├── main.py
├── requirements.txt
├── README.md
└── website/
```

---

# Konfigurasi

Konfigurasi utama berada di file:

```
main.py
```

Bagian:

```python
WAYBACK = "https://web.archive.org"

TIMEOUT = 40

DELAY = 0.5
```

## WAYBACK

URL Internet Archive.

Default:

```python
WAYBACK = "https://web.archive.org"
```

---

## TIMEOUT

Batas waktu request.

Default:

```python
TIMEOUT = 40
```

Jika koneksi lambat, bisa diperbesar.

Contoh:

```python
TIMEOUT = 90
```

---

## DELAY

Jeda antar download.

Default:

```python
DELAY = 0.5
```

Nilai lebih besar akan mengurangi beban request.

---

# Catatan

* Tidak semua website dapat dikembalikan 100%.
* Hanya data yang tersedia di Wayback Machine yang dapat diambil.
* Website yang menggunakan database, API, login, atau sistem dinamis tidak akan kembali secara penuh.
* Beberapa file mungkin tidak tersedia karena tidak pernah diarsipkan.
* Jumlah halaman tergantung data yang tersedia di Wayback.

---

# Teknologi

Project ini menggunakan:

* Python
* Requests
* BeautifulSoup4
* tqdm
* Internet Archive Wayback CDX API

---

# Lisensi

Gunakan dengan bijak.
Pastikan memiliki izin sebelum melakukan clone terhadap website yang bukan milik sendiri.
