# 🪟 Panduan Cross-Compilation / Build Aplikasi Windows (.exe 64-bit)

Aplikasi Python yang menggunakan pustaka C/C++ native seperti **OpenCV** dan **MediaPipe** (beserta runtime TensorFlow Lite-nya) **harus di-compile di lingkungan sistem operasi Windows 64-bit**. 

Penjelasan singkat mengapa tidak bisa di-compile langsung dari Linux:
- PyInstaller bundling library biner (.dll/.so). Menjalankan PyInstaller di Linux akan membungkus library Linux (`.so`), bukan executable Windows (`.exe` / `.dll`).
- MediaPipe menggunakan library C++ terkompilasi khusus platform.

---

## 🚀 Cara Build di Mesin / VM Windows 64-bit

Ikuti langkah-langkah mudah berikut di komputer bertipe Windows (x64):

### 1. Persiapan Lingkungan
1. Install **Python 3.10 atau 3.11 (64-bit)** dari [python.org](https://www.python.org/downloads/). Pastikan mencentang *"Add Python to PATH"*.
2. Clone / Copy folder project `foto-kita-blur` ini ke mesin Windows.

### 2. Install Dependencies & Build
Buka **Command Prompt (cmd)** atau **PowerShell** di dalam folder project `foto-kita-blur`, lalu jalankan:

```cmd
:: 1. Buat dan aktifkan virtual environment (Opsional tapi disarankan)
python -m venv .venv
.venv\Scripts\activate

:: 2. Install dependency
pip install -r requirements.txt

:: 3. Download model file ke folder assets (jika belum ada)
curl -o assets\hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task

:: 4. Jalankan Kompilasi PyInstaller
pyinstaller build\build_windows.spec
```

### 3. Hasil Output
Setelah proses build selesai, file `.exe` standalone 64-bit dapat ditemukan di folder:
📂 **`dist\FotoKitaBlur.exe`**

File `FotoKitaBlur.exe` ini sudah berisi semua dependency, model MediaPipe, dan OpenCV sehingga dapat langsung dijalankan di komputer Windows 64-bit manapun tanpa perlu install Python lagi!

---

## 🤖 Opsi Alternatif: Automatic Build via GitHub Actions (CI/CD)

Jika Anda tidak memiliki komputer Windows, Anda bisa memanfaatkan **GitHub Actions** gratis untuk melakukan compile otomatis setiap kali membuat Release / Push.

Buat file `.github/workflows/build_windows.yml`:

```yaml
name: Build Windows Executable

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          architecture: 'x64'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Download MediaPipe Model
        run: |
          curl -o assets/hand_landmarker.task https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task

      - name: Build with PyInstaller
        run: |
          pyinstaller build/build_windows.spec

      - name: Upload Artifact
        uses: actions/upload-artifact@v4
        with:
          name: FotoKitaBlur-Windows-x64
          path: dist/FotoKitaBlur.exe

```
