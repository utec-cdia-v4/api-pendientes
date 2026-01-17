# models.py
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
import enum
from database import Base

class ImportanciaEnum(str, enum.Enum):
    alta = "alta"
    media = "media"
    baja = "baja"

class EstadoEnum(str, enum.Enum):
    pendiente = "pendiente"
    completado = "completado"

class Pendiente(Base):
    __tablename__ = "pendientes"

    id = Column(Integer, primary_key=True, index=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    descripcion = Column(String, nullable=False)
    importancia = Column(Enum(ImportanciaEnum), default=ImportanciaEnum.media)
    estado = Column(Enum(EstadoEnum), default=EstadoEnum.pendiente)
    fecha_atencion = Column(DateTime, nullable=True)
