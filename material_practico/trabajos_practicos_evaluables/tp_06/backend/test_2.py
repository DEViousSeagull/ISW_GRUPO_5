import pytest
from entidades.compra import Compra
from entidades.entrada import Entrada
from datetime import date
def test_compra_cantidad_entradas_invalida():
        entradas = [Entrada(id=i, precio=100, tipo_Entrada="General", edad_Visitante=18) for i in range(11)]
        compra = Compra(fecha=date.today(), entradas=entradas, monto_total=1100)
        with pytest.raises(ValueError) as e:
            compra.cantidad_entradas
        assert str(e.value) == "Cantidad inválida; máximo 10"



