# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from database import SessionLocal, engine, Base
from models import Pendiente, EstadoEnum
from schemas import PendienteCreate, PendienteUpdate, PendienteOut

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Pendientes")

origins = [
    "http://localhost",
    "http://127.0.0.1",
    # agrega aquí el origen donde sirvas el index.html si usas algún servidor
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/pendientes", response_model=List[PendienteOut])
def listar_pendientes(db: Session = Depends(get_db)):
    return db.query(Pendiente).order_by(Pendiente.fecha_creacion.desc()).all()

@app.post("/pendientes", response_model=PendienteOut)
def crear_pendiente(p: PendienteCreate, db: Session = Depends(get_db)):
    nuevo = Pendiente(
        descripcion=p.descripcion,
        importancia=p.importancia,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.put("/pendientes/{pendiente_id}", response_model=PendienteOut)
def actualizar_pendiente(pendiente_id: int, data: PendienteUpdate, db: Session = Depends(get_db)):
    pendiente = db.query(Pendiente).filter(Pendiente.id == pendiente_id).first()
    if not pendiente:
        raise HTTPException(status_code=404, detail="Pendiente no encontrado")

    if data.descripcion is not None:
        pendiente.descripcion = data.descripcion
    if data.importancia is not None:
        pendiente.importancia = data.importancia
    if data.estado is not None:
        pendiente.estado = data.estado
        if data.estado == EstadoEnum.completado:
            pendiente.fecha_atencion = datetime.utcnow()
        else:
            pendiente.fecha_atencion = None

    db.commit()
    db.refresh(pendiente)
    return pendiente

@app.delete("/pendientes/{pendiente_id}")
def eliminar_pendiente(pendiente_id: int, db: Session = Depends(get_db)):
    pendiente = db.query(Pendiente).filter(Pendiente.id == pendiente_id).first()
    if not pendiente:
        raise HTTPException(status_code=404, detail="Pendiente no encontrado")
    db.delete(pendiente)
    db.commit()
    return {"ok": True}
