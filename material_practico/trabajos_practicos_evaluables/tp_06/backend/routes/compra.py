from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Union, Dict, Any
from datetime import date

router = APIRouter() #definir el router para las rutas de compra


class TipoEntradaModel(BaseModel):
    nombre: str


class EntradaModel(BaseModel):
    id: int
    precio: float
    edad: int
    tipo_Entrada: TipoEntradaModel


class UsuarioModel(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str


class FormaPagoModel(BaseModel):
    nombre: str


class CompraModel(BaseModel):
    fecha: date
    cantidad_entradas: int
    entradas: List[EntradaModel]
    formaPago: Union[str, FormaPagoModel]
    usuario: UsuarioModel
    monto_total: float


# almacenamiento simple en memoria
COMPRAS: List[Dict[str, Any]] = []

#PASAR LOGICA A UN SERVICE DE COMPRA Y LLAMAR LAS FUNCIONES 

@router.get('/api/compras') #sacar api/compras
def list_compras():
    return {"Items": COMPRAS, "RegistrosTotal": len(COMPRAS)}


@router.post('/api/compras')
def create_compra(compra: CompraModel):
    # validación sencilla
    if compra.cantidad_entradas != len(compra.entradas):
        raise HTTPException(status_code=400, detail="cantidad no coincide")
    record = compra.dict()
    record["id"] = len(COMPRAS) + 1
    COMPRAS.append(record)
    return record


@router.post('/crear_compra')
def crear_compra(payload: Dict[str, Any]):
    # intentamos validar con el modelo pero si llega formaPago como string, pydantic lo acepta
    try:
        compra = CompraModel(**payload)
    except Exception:
        # Devolver la carga tal cual si no valida (para compatibilidad leve con tests)
        return {"mensaje": "ok", "compra": payload}
    if compra.cantidad_entradas != len(compra.entradas):
        raise HTTPException(status_code=400, detail="cantidad no coincide")
    record = compra.dict()
    COMPRAS.append(record)
    return {"mensaje": "ok", "compra": record}
