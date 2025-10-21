from sqlalchemy.orm import Session
from sqlalchemy import select
from engine import engine
from entidades.compra import Compra
from entidades.entrada import Entrada 
from sqlalchemy.orm import joinedload  


class CompraService:
    #@staticmethod
    # def get_all():
    #     """Devuelve todas las formas de pago en formato lista de dicts"""
    #     with Session(engine) as session:
    #         compras = session.scalars(select(Compra)).all()
    #         return [{"id": c.id, "fecha": c.fecha, "cantidad_entradas": c.cantidad_entradas, "monto_total": c.monto_total, "forma_pago": c.forma_pago, "usuario": c.usuario_id, "mercado_pago": c.mercado_pago_redirect_url} for c in compras]
       
    @staticmethod
    def get_all() -> list[dict]:
        with Session(engine) as session:
            # Carga todas las relaciones asociadas
            compras = session.query(Compra).options(
                joinedload(Compra.usuario),
                joinedload(Compra.forma_pago),
                joinedload(Compra.entradas).joinedload(Entrada.tipo_entrada)
            ).all()

            # Convertimos a formato JSON-friendly
            resultado = []
            for c in compras:
                resultado.append({
                    "id": c.id,
                    "fecha": c.fecha.isoformat() if c.fecha else None,
                    "cantidad_entradas": c.cantidad_entradas,
                    "monto_total": c.monto_total,
                    "forma_pago": {
                        "id": c.forma_pago.id if c.forma_pago else None,
                        "nombre":c.forma_pago.nombre if c.forma_pago else None,
                    },
                    "usuario": {
                        "id": c.usuario.id if c.usuario else None,
                        "nombre": c.usuario.nombre if c.usuario else None,
                        "apellido": c.usuario.apellido if c.usuario else None,
                        "email": c.usuario.email if c.usuario else None,
                    },
                    "entradas": [
                        {
                            "id": e.id,
                            "precio": e.precio_unitario,
                            "edad": e.edad,
                            "tipo_entrada": {
                                "nombre": e.tipo_entrada.nombre if e.tipo_entrada else None
                            }
                        }
                        for e in c.entradas
                    ],
                })
            return resultado
   
    def post_compra(compra: Compra) -> Compra:
        with Session(engine) as session:
            session.add(compra)
            session.commit()
            session.refresh(compra)
            return compra
       
