import pytest
from entidades.compra import Compra
from entidades.entrada import Entrada
from entidades.tipoEntrada import TipoEntrada
from datetime import date

from material_practico.trabajos_practicos_evaluables.tp_06.backend.entidades.tipoEntrada import TipoEntrada
def test_compra_cantidad_entradas_invalida():
        tipo=TipoEntrada(nombre="Regular")
        entradas = [Entrada(id=i, precio=5000, tipo_Entrada=tipo, edad=18) for i in range(11)]
        compra = Compra(fecha=date.today(), entradas=entradas, monto_total=1100)
        with pytest.raises(ValueError) as e:
            compra.cantidad_entradas
        assert str(e.value) == "Cantidad inválida; máximo 10"

def test_compra_cantidad_entradas_valida():
        tipo = TipoEntrada(nombre="Regular")
        entradas = [Entrada(id=i, precio=5000, tipo_Entrada=tipo, edad=18) for i in range(5)]
        compra = Compra(fecha=date.today(), entradas=entradas, monto_total=5000)
        assert compra.cantidad_entradas == 5

# def test_compra_sin_entradas_levanta_error():
#     compra = Compra(fecha=date.today(), monto_total=1100)
#     with pytest.raises(ValueError) as e:
#         _ = compra.cantidad_entradas
#     assert "entrad" in str(e.value).lower()

def test_menor_de_diez_paga_mitad():
            tipo = TipoEntrada(nombre="Regular")
            entrada_menor = Entrada(id=1, precio=5000, edad=9, tipo_Entrada=tipo)
            # Suponemos que el método calcular_precio aplica el descuento
            entrada_menor.calcular_precio()
            assert entrada_menor.precio == 2500
def test_menor_de_tres_no_paga():
            tipo = TipoEntrada(nombre="Regular")
            entrada_bebe = Entrada(id=2, precio=5000, edad=2, tipo_Entrada=tipo)
            # Suponemos que el método calcular_precio aplica el descuento
            entrada_bebe.calcular_precio()
            assert entrada_bebe.precio == 0

def test_mayor_de_sesenta_paga_mitad():
            tipo = TipoEntrada(nombre="Regular")
            entrada_mayor = Entrada(id=3, precio=5000, edad=61, tipo_Entrada=tipo)
            # Suponemos que el método calcular_precio aplica el descuento
            entrada_mayor.calcular_precio()
            assert entrada_mayor.precio == 2500

def test_entre_10_y_60_paga_completo():
            tipo = TipoEntrada(nombre="Regular")
            entrada_adulto = Entrada(id=4, precio=5000, edad=30, tipo_Entrada=tipo)
            # Suponemos que el método calcular_precio no aplica descuento
            entrada_adulto.calcular_precio()
            assert entrada_adulto.precio == 5000

def test_VIP_menor_de_diez_paga_mitad():
            tipo = TipoEntrada(nombre="VIP")
            entrada_menor = Entrada(id=1, precio=5000, edad=9, tipo_Entrada=tipo)
            # Suponemos que el método calcular_precio aplica el descuento
            entrada_menor.calcular_precio()
            assert entrada_menor.precio == 5000  # Porque VIP siempre es 10000, no importa la edad
def test_VIP_menor_de_tres_no_paga():
            tipo = TipoEntrada(nombre="VIP")
            entrada_bebe = Entrada(id=2, precio=5000, edad=2, tipo_Entrada=tipo)
            # Suponemos que el método calcular_precio aplica el descuento
            entrada_bebe.calcular_precio()
            assert entrada_bebe.precio == 0

def test_VIP_mayor_de_sesenta_paga_mitad():
            tipo = TipoEntrada(nombre="VIP")
            entrada_mayor = Entrada(id=3, precio=5000, edad=61, tipo_Entrada=tipo)
            # Suponemos que el método calcular_precio aplica el descuento
            entrada_mayor.calcular_precio()
            assert entrada_mayor.precio == 5000  

def test_VIP_entre_10_y_60_paga_completo():
            tipo = TipoEntrada(nombre="VIP")
            entrada_adulto = Entrada(id=4, precio=5000, edad=30, tipo_Entrada=tipo)
            # Suponemos que el método calcular_precio no aplica descuento
            entrada_adulto.calcular_precio()
            assert entrada_adulto.precio == 10000