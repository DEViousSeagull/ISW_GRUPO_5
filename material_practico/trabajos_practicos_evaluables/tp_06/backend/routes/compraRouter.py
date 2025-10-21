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
    # Import here to avoid changing top-of-file imports

    # Validar/convertir payload a la entidad Esperada por el service
    try:
        compra = Compra(**payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Datos de entrada inválidos: {e}")

    try:
        result = CompraService.post_compra(compra)
    except HTTPException:
        raise
    except Exception as e:
        # Errores del service que no sean HTTPException -> 500
        raise HTTPException(status_code=500, detail=str(e))
    return result
