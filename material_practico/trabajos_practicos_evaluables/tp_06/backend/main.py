from fastapi import FastAPI
from routes.compra import router as compra_router

app = FastAPI()
app.include_router(compra_router)


@app.get('/crear_pago')
def crear_pago():
    return {"url_pago": "https://sandbox.mercadopago.com/checkout/v1/redirect?pref_id=MOCK_123"}


@app.post('/enviar_mail')
def enviar_mail(payload: dict):
    # simulamos envío
    return {"mensaje": "enviado", "email": payload.get("email")}
