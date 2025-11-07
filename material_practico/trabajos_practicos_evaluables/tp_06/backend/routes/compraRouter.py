from fastapi import APIRouter, HTTPException
from services.compraService import CompraService


router = APIRouter(prefix="/compras", tags=["Compras"])

@router.get("/", summary="Obtener todas las compras")
def get_compras():
    compras = CompraService.get_all()
    if not compras:
        raise HTTPException(status_code=404, detail="No se encontraron compras")
    return compras


@router.post('/crear_compra', summary="Crear una compra")
def crear_compra(payload: dict):
    try:
        result = CompraService.post_compra(payload)
    except HTTPException:
        raise
    except Exception as e:
        # Errores del service que no sean HTTPException -> 500
        raise HTTPException(status_code=500, detail=str(e))
    return result
