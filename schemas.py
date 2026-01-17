# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models import ImportanciaEnum, EstadoEnum

class PendienteBase(BaseModel):
    descripcion: str
    importancia: ImportanciaEnum = ImportanciaEnum.media

class PendienteCreate(PendienteBase):
    pass

class PendienteUpdate(BaseModel):
    descripcion: Optional[str] = None
    importancia: Optional[ImportanciaEnum] = None
    estado: Optional[EstadoEnum] = None

class PendienteOut(BaseModel):
    id: int
    fecha_creacion: datetime
    descripcion: str
    importancia: ImportanciaEnum
    estado: EstadoEnum
    fecha_atencion: Optional[datetime] = None

    class Config:
        orm_mode = True
