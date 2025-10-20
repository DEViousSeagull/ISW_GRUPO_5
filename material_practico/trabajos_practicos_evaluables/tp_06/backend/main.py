from fastapi import FastAPI
from routes.compra import router as compra_router
from routes.tipoEntradaRouter import router as tipoEntrada_router
import uvicorn

from sqlalchemy.orm import DeclarativeBase
from setup import bootstrap


app = FastAPI()
app.include_router(compra_router)
app.include_router(tipoEntrada_router)


@app.get('/crear_pago')
def crear_pago():
    return {"url_pago": "https://sandbox.mercadopago.com/checkout/v1/redirect?pref_id=MOCK_123"}


@app.post('/enviar_mail')
def enviar_mail(payload: dict):
    # simulamos envío
    return {"mensaje": "enviado", "email": payload.get("email")}



if __name__ == "__main__":
    bootstrap()
    # Ejecuta el backend en localhost:8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
    
# ...existing code...

