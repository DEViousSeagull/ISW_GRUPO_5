from sqlalchemy.orm import Session
from sqlalchemy import select
from engine import engine
from entidades.tipoEntrada import TipoEntrada

class TipoEntradaService:
    """Servicio básico de Tipos de Entrada"""

    @staticmethod
    def get_all():
        """Devuelve todos los tipos de entrada en formato lista de dicts"""
        with Session(engine) as session:
            tipos = session.scalars(select(TipoEntrada)).all()
            return [{"id": t.id, "nombre": t.nombre} for t in tipos]
    