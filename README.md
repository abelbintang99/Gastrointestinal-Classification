# BelzClassification: Medical Diagnosis Support

## Struktur Proyek
- `/backend`: FastAPI, AI Logic, & SQLite Database.
- `/frontend`: Vue.js 3 + Vite Dashboard.

Aplikasi Full-stack yang membantu klasifikasi kondisi medis Gastrointestinal menggunakan Machine Learning. Aplikasi ini dirancang untuk memberikan referensi cepat bagi tenaga medis melalui analisis gambar endoskopi.

##  Fitur Utama
- **Classification**: Deteksi kondisi seperti Kolitis secara real-time.
- **Secure Management**: Registrasi & Login user dengan keamanan JWT.
- **Persistent History**: Menyimpan riwayat diagnosa langsung ke database.
- **Modern Interface**: Dashboard responsif dengan preview gambar medis.

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, Pydantic, Python.
- **Frontend**: Vue.js 3 (Vite), Axios, CSS3 Modern.
- **ML Integration**: Model klasifikasi gambar terintegrasi.

##  Cara Menjalankan Lokal
1. **Clone Repo**: `git clone https://github.com/abelbintang99/Gastrointestinal-Classification.git`
2. **Setup Backend**:
   - `cd backend`
   - `pip install -r requirements.txt`
   - `python main.py`
3. **Setup Frontend**:
   - `cd frontend`
   - `npm install`
   - `npm run dev`

## Disclaimer
Aplikasi ini hanya untuk tujuan edukasi. Diagnosa medis akhir harus selalu dilakukan oleh profesional medis bersertifikat.
