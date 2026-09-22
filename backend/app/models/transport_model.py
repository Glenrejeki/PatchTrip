from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base  # Menggunakan Base dari session database yang baru dibuat

class TransportRouteModel(Base):
    __tablename__ = "transport_routes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transport_type = Column(String(50), nullable=False)
    provider_name = Column(String(100), nullable=False)
    origin_city = Column(String(100), nullable=False)
    destination_city = Column(String(100), nullable=False)
    base_price = Column(Numeric(10, 2), nullable=True)

    schedules = relationship("TransportScheduleModel", back_populates="route", cascade="all, delete-orphan")


class TransportScheduleModel(Base):
    __tablename__ = "transport_schedules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    route_id = Column(Integer, ForeignKey("transport_routes.id", ondelete="CASCADE"), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    status = Column(String(50), default="AVAILABLE")

    route = relationship("TransportRouteModel", back_populates="schedules")