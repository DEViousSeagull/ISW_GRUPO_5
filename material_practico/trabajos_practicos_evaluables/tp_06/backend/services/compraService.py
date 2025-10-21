from sqlalchemy.orm import Session
from sqlalchemy import select
from engine import engine
from entidades.compra import Compra
from entidades.entrada import Entrada 
from sqlalchemy.orm import joinedload  
from datetime import date


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
   
    @staticmethod
    def post_compra(data: dict) -> dict:
        with Session(engine) as session:
            # Crear nueva compra
            nueva_compra = Compra(
                fecha=date.fromisoformat(data["fecha"]),
                cantidad_entradas=data["cantidad_entradas"],
                monto_total=data["monto_total"],
                usuario_id=data["usuario"]["id"],
                forma_pago_id=data["forma_pago"]["id"]
            )
            
            # Agregar entradas
            for entrada_data in data["entradas"]:
                entrada = Entrada(
                    precio_unitario=entrada_data["precio_unitario"],
                    edad=entrada_data["edad"],
                    tipo_entrada_id=entrada_data["tipo_entrada"]["id"]
                )
                nueva_compra.entradas.append(entrada)
            
            session.add(nueva_compra)
            session.commit()
            session.refresh(nueva_compra)
            
            # Retornar respuesta formateada
            return {
                "mensaje": "Compra creada exitosamente",
                "compra": {
                    "id": nueva_compra.id,
                    "fecha": nueva_compra.fecha.isoformat(),
                    "cantidad_entradas": nueva_compra.cantidad_entradas,
                    "monto_total": nueva_compra.monto_total,
                    "forma_pago": {
                        "id": nueva_compra.forma_pago.id,
                        "nombre": nueva_compra.forma_pago.nombre
                    },
                    "usuario": {
                        "id": nueva_compra.usuario.id,
                        "nombre": nueva_compra.usuario.nombre,
                        "apellido": nueva_compra.usuario.apellido,
                        "email": nueva_compra.usuario.email
                    }
                }
            }
