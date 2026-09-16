import logging
import sys

def setup_logger(name: str = "PatchTrip") -> logging.Logger:
    """
    Mengatur dan mengonfigurasi logger global untuk aplikasi PatchTrip backend.
    Menghasilkan format log yang terstruktur dengan informasi waktu dan level pesan.
    """
    logger = logging.getLogger(name)
    
    # Mencegah penambahan handler berulang jika logger dipanggil berkali-kali
    if logger.handlers:
        return logger

    # Menetapkan level log minimum yang akan dicatat (INFO ke atas)
    logger.setLevel(logging.INFO)

    # Format penulisan log: [Waktu] [Level Log] [Nama Modul]: Pesan
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler untuk mencetak log langsung ke konsol / terminal standar (stdout)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    
    # Menambahkan handler ke objek logger
    logger.addHandler(stream_handler)

    return logger

# Instansiasi objek logger utama yang siap diimpor dan digunakan di seluruh modul backend
logger = setup_logger()