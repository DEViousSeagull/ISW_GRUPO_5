import uuid

class MercadoPagoClient:
    def generate_redirect(self, compra_id: str) -> str:
        pref_id = uuid.uuid4().hex[:12].upper()
        # simulación sandbox
        return f"https://sandbox.mercadopago.com/checkout/v1/redirect?pref_id=MOCK_{pref_id}"
