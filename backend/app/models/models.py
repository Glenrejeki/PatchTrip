from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    """
    Model SQLAlchemy untuk entitas Pengguna (User).
    Menyimpan data dasar akun pengguna yang menggunakan sistem rekomendasi PatchTrip.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relasi ORM: Satu pengguna memiliki banyak riwayat perjalanan dan itinerary tersimpan
    histories = relationship("TravelHistory", back_populates="user", cascade="all, delete-orphan")
    itineraries = relationship("Itinerary", back_populates="user", cascade="all, delete-orphan")


class POI(Base):
    """
    Model SQLAlchemy untuk Point of Interest (POI) / Destinasi Wisata.
    Merujuk pada basis data destinasi dunia nyata (mengadaptasi benchmark TripTailor)[cite: 3].
    """
    __tablename__ = "pois"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=True)  # Contoh: Sejarah, Alam, Pantai, Budaya
    description = Column(Text, nullable=True)
    location = Column(String, index=True, nullable=True)   # Kota atau Wilayah
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)


class TravelHistory(Base):
    """
    Model SQLAlchemy untuk Riwayat Perjalanan Pengguna (Long-Term History).
    Menyimpan rekam jejak kunjungan historis yang nantinya akan diproses 
    oleh modul Hierarchical Patch Compression[cite: 3].
    """
    __tablename__ = "travel_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trip_name = Column(String, nullable=False)             # Nama/Judul perjalanan masa lalu
    visit_date = Column(DateTime, nullable=True)
    details = Column(Text, nullable=True)                  # Deskripsi atau daftar kunjungan mentah (item patch)

    # Relasi ke tabel User
    user = relationship("User", back_populates="histories")


class Itinerary(Base):
    """
    Model SQLAlchemy untuk Hasil Rekomendasi Itinerary Wisata.
    Menyimpan hasil akhir generasi teks dari modul RAG & Qwen3-8B[cite: 3].
    """
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)                 # Judul itinerary (misal: "Liburan Budaya di Yogyakarta")
    duration_days = Column(Integer, nullable=False)        # Durasi perjalanan dalam hari
    budget = Column(String, nullable=True)                 # Kategori anggaran (misal: Hemat, Menengah, Mewah)
    content = Column(Text, nullable=False)                 # Teks lengkap hasil generate itinerary (format markdown/json)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relasi ke tabel User
    user = relationship("User", back_populates="itineraries")