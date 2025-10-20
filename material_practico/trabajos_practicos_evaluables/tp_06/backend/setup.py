from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Float, Date, Text, func, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from entidades.compra import Compra
from entidades.entrada import Entrada
from entidades.formaPago import FormaPago
from entidades.tipoEntrada import TipoEntrada
from entidades.usuario import Usuario
from entidades.base import Base
from engine import engine
from sqlalchemy.orm import Session

def reset_db():
    print("Reseteando base de datos...")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("Tablas recreadas.")

def bootstrap():
    Base.metadata.create_all(engine)

    with Session(engine) as s:
        # seeds: formas de pago
        if not s.scalar(select(func.count(FormaPago.id))):
            s.add_all([FormaPago(nombre="Efectivo"), FormaPago(nombre="Tarjeta")])

        # seeds: tipos de pase
        if not s.scalar(select(func.count(TipoEntrada.id))):
            s.add_all([TipoEntrada(nombre="VIP"), TipoEntrada(nombre="General")])

        # seed: usuario
        if not s.scalar(select(func.count(Usuario.id))):
            s.add(Usuario(nombre="Juan", apellido="Pérez", email="juan@example.com"))

        s.commit()

        # seeds: entradas
        # if not s.scalar(select(func.count(Entrada.id))):
        #     vip = s.scalar(select(TipoEntrada).where(TipoEntrada.nombre == "VIP"))
        #     gen = s.scalar(select(TipoEntrada).where(TipoEntrada.nombre == "General"))
        #     s.add_all([
        #         Entrada(id=100, edad=30, tipo_entrada_id=gen.id, precio_unitario=5000.0),
        #         Entrada(id=101, edad=12, tipo_entrada_id=gen.id, precio_unitario=5000.0),
        #     ])
        #     s.commit()