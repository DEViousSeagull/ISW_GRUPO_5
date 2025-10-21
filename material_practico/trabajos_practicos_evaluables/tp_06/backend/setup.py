from datetime import date

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

        # ------------------------------------------------------------------
        # Crear una compra con 1 entrada General (precio 5000)
        # ------------------------------------------------------------------
        if s.scalar(select(func.count(Compra.id))):
            return  # ya hay compras
        
        # Obtener las entidades necesarias
        usuario = s.scalar(select(Usuario).where(Usuario.email == "juan@example.com"))
        forma_pago = s.scalar(select(FormaPago).where(FormaPago.nombre == "Efectivo"))
        tipo_general = s.scalar(select(TipoEntrada).where(TipoEntrada.nombre == "General"))

        if usuario and forma_pago and tipo_general:
            compra = Compra(
                fecha=date.today(),
                cantidad_entradas=1,
                monto_total=5000.0,
                forma_pago_id=forma_pago.id,
                usuario_id=usuario.id,
            )

            # Crear entrada asociada
            entrada = Entrada(
                edad=30,
                tipo_entrada_id=tipo_general.id,
                precio_unitario=5000.0,
                compra=compra,  # asocia la entrada con la compra
            )

            s.add(compra)
            s.add(entrada)
            s.commit()

            print("Compra de ejemplo creada con 1 entrada General (5000).")
        else:
            print("No se pudieron encontrar las entidades necesarias para crear la compra.")