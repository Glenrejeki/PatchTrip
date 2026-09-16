# Menggunakan base image resmi Python versi 3.10 yang ringan (slim)
FROM python:3.10-slim

# Menetapkan environment variables agar Python tidak membuat file .pyc 
# dan langsung mencetak output log ke terminal tanpa buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Menetapkan direktori kerja utama di dalam container
WORKDIR /app

# Menginstaldependencies sistem dasar yang sering dibutuhkan pustaka AI/ML (seperti build-essential, git, dll)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Menyalin file daftar dependensi ke dalam container
COPY requirements.txt .

# Menginstal pustaka Python (termasuk FastAPI, LangChain, FAISS, PyTorch, dll)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode sumber backend ke dalam direktori kerja container
COPY . .

# Mengekspos port standar FastAPI (port 8000)
EXPOSE 8000

# Perintah default untuk menjalankan server Uvicorn FastAPI di dalam container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]