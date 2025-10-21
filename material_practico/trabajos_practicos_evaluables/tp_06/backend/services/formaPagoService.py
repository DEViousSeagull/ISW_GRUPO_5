from sqlalchemy.orm import Session
from sqlalchemy import select
from engine import engine
from entidades.formaPago import FormaPago

class FormaPagoService:
    
    @staticmethod
    def get_all():
        """Devuelve todas las formas de pago en formato lista de dicts"""
        with Session(engine) as session:
            formas_pago = session.scalars(select(FormaPago)).all()
            return [{"id": fp.id, "nombre": fp.nombre} for fp in formas_pago]