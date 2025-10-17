import pytest
from entidades.compra import Compra
from entidades.entrada import Entrada
from entidades.tipoEntrada import TipoEntrada
from datetime import date

from material_practico.trabajos_practicos_evaluables.tp_06.backend.entidades.tipoEntrada import TipoEntrada
def test_compra_cantidad_entradas_invalida():
        tipo=TipoEntrada(nombre="Regular")
        entradas = [Entrada(id=i, precio=100, tipo_Entrada=tipo, edad=18) for i in range(11)]
        compra = Compra(fecha=date.today(), entradas=entradas, monto_total=1100)
        with pytest.raises(ValueError) as e:
            compra.cantidad_entradas
        assert str(e.value) == "Cantidad inválida; máximo 10"

def test_compra_cantidad_entradas_valida():
        tipo = TipoEntrada(nombre="Regular")
        entradas = [Entrada(id=i, precio=100, tipo_Entrada=tipo, edad=18) for i in range(5)]
        compra = Compra(fecha=date.today(), entradas=entradas, monto_total=500)
        assert compra.cantidad_entradas == 5

# def test_compra_sin_entradas_levanta_error():
#     compra = Compra(fecha=date.today(), monto_total=1100)
#     with pytest.raises(ValueError) as e:
#         _ = compra.cantidad_entradas
#     assert "entrad" in str(e.value).lower()

def test_menor_de_diez_paga_mitad():
            tipo = TipoEntrada(nombre="Regular")
            entrada_menor = Entrada(id=1, precio=100, edad=9, tipo_Entrada=tipo)
            # Suponemos que el método calcular_precio aplica el descuento
            entrada_menor.calcular_precio()
            assert entrada_menor.precio == 50