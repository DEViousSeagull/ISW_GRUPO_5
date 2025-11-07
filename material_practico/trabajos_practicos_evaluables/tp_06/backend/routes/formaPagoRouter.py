from fastapi import APIRouter, HTTPException
from services.formaPagoService import FormaPagoService

router = APIRouter(prefix="/formas_pago", tags=["Formas de Pago"])

@router.get("/", summary="Obtener todas las formas de pago")
def get_formas_pago():
    formas = FormaPagoService.get_all()
    if not formas:
        raise HTTPException(status_code=404, detail="No se encontraron formas de pago")
    return formas