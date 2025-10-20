from fastapi import APIRouter, HTTPException
from services.tipoEntradaService import TipoEntradaService

router = APIRouter(prefix="/tipos-entrada", tags=["Tipos de Entrada"])

@router.get("/", summary="Obtener todos los tipos de entrada")
def get_tipos_entrada():
    tipos = TipoEntradaService.get_all()
    if not tipos:
        raise HTTPException(status_code=404, detail="No se encontraron tipos de pase")
    return tipos