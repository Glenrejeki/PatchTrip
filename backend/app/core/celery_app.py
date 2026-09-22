from celery import Celery

# Inisialisasi Celery dengan broker Redis lokal
celery_app = Celery(
    "patchtrip_worker",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Konfigurasi agar Celery otomatis mendiskusikan tugas dan zona waktu
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Jakarta",
    enable_utc=False,
)

# Pengaturan Jadwal Otomatis (Periodic Task / Cron Schedule)
# Contoh: Menjalankan tugas scraping otomatis setiap hari pukul 02:00 pagi
celery_app.conf.beat_schedule = {
    'scrape-transport-every-night': {
        'task': 'app.tasks.transport_task.run_transport_scraper',
        'schedule': 86400.0, # 86400 detik = 24 jam sekali (atau gunakan crontab)
    },
}