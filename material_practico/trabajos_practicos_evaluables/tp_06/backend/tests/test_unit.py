import json
import pytest
from entidades.compra import Compra
from entidades.entrada import Entrada
from entidades.tipoEntrada import TipoEntrada
from datetime import date
from entidades.formaPago import FormaPago
from entidades.mercado_pago import MercadoPagoClient
from entidades.usuario import Usuario

# -------------------- FIXTURES --------------------

@pytest.fixture
def tipo_vip():
    return TipoEntrada(id=1, nombre="VIP")

@pytest.fixture
def tipo_general():
    return TipoEntrada(id=2, nombre="General")

@pytest.fixture
def usuario_ana():
    return Usuario(id=1, nombre="Ana", apellido="Perez", email="ana.perez@example.com")

@pytest.fixture
def usuario_luis():
    return Usuario(id=2, nombre="Luis", apellido="Gomez", email="luis.gomez@example.com")

@pytest.fixture
def forma_pago_efectivo():
    return FormaPago(id=1, nombre="Efectivo")

@pytest.fixture
def forma_pago_tarjeta():
    return FormaPago(id=2, nombre="Tarjeta")

# -------------------- TESTS --------------------

# --- CANTIDAD DE ENTRADAS ---
def test_compra_cantidad_entradas_invalida(tipo_general, forma_pago_efectivo, usuario_ana):
    entradas = [Entrada(id=i, precio_unitario=5000, tipo_entrada=tipo_general, edad=18, tipo_entrada_id=tipo_general.id) for i in range(11)]
    compra = Compra(
        id=2,
        fecha=date.today(),
        cantidad_entradas=11,
        entradas=entradas,
        forma_pago=forma_pago_efectivo,
        usuario=usuario_ana,
        monto_total=1100,
        forma_pago_id=forma_pago_efectivo.id,
        usuario_id=usuario_ana.id
    )
    with pytest.raises(ValueError) as e:
        compra.cantidad_entradas_validas()
    assert str(e.value) == "Cantidad inválida; máximo 10"


def test_compra_cantidad_entradas_valida(tipo_general, forma_pago_efectivo, usuario_ana):
    entradas = [Entrada(id=i, precio_unitario=5000, tipo_entrada=tipo_general, edad=18, tipo_entrada_id=tipo_general.id) for i in range(10)]
    compra = Compra(
        id=1,
        fecha=date.today(),
        cantidad_entradas=10,
        entradas=entradas,
        forma_pago=forma_pago_efectivo,
        usuario=usuario_ana,
        monto_total=5000,
        forma_pago_id=forma_pago_efectivo.id,
        usuario_id=usuario_ana.id
    )
    assert compra.cantidad_entradas == 10

# --- PRECIO SEGÚN EDAD ---
@pytest.mark.parametrize("edad,expected", [
    (9, 2500),
    (2, 0),
    (61, 2500),
    (30, 5000)
])
def test_precio_general(tipo_general, edad, expected):
    entrada = Entrada(id=1, precio_unitario=5000, edad=edad, tipo_entrada=tipo_general, tipo_entrada_id=tipo_general.id)
    entrada.calcular_precio()
    assert entrada.precio_unitario == expected

@pytest.mark.parametrize("edad,expected", [
    (9, 5000),
    (2, 0),
    (61, 5000),
    (30, 10000)
])
def test_precio_vip(tipo_vip, edad, expected):
    entrada = Entrada(id=1, precio_unitario=5000, edad=edad, tipo_entrada=tipo_vip, tipo_entrada_id=tipo_vip.id)
    entrada.calcular_precio()
    assert entrada.precio_unitario == expected

# --- CREACION DE OBJETOS ---
def test_crear_entrada_tiene_todos_sus_atributos(tipo_general):
    entrada = Entrada(id=10, precio_unitario=5000, edad=25, tipo_entrada=tipo_general, tipo_entrada_id=tipo_general.id)
    assert entrada.id == 10
    assert entrada.precio_unitario == 5000
    assert entrada.edad == 25
    assert entrada.tipo_entrada is tipo_general
    assert isinstance(entrada.tipo_entrada, TipoEntrada)
    assert isinstance(entrada, Entrada)

def test_crear_compra_tiene_atributos_y_valores(tipo_general, forma_pago_efectivo, usuario_ana):
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo_general, tipo_entrada_id=tipo_general.id)]
    compra = Compra(
        id=1,
        fecha=date.today(),
        cantidad_entradas=1,
        entradas=entradas,
        forma_pago=forma_pago_efectivo,
        usuario=usuario_ana,
        monto_total=5000,
        forma_pago_id=forma_pago_efectivo.id,
        usuario_id=usuario_ana.id
    )
    assert compra.monto_total == 5000
    assert isinstance(compra, Compra)
    assert all(isinstance(e, Entrada) for e in compra.entradas)

# --- VALIDACIONES FECHA ---
def test_fecha_compra_es_menor_actual_falla(tipo_general, forma_pago_efectivo, usuario_ana):
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo_general, tipo_entrada_id=tipo_general.id)]
    compra = Compra(
        id=4,
        fecha=date(2020, 3, 1),
        cantidad_entradas=1,
        entradas=entradas,
        forma_pago=forma_pago_efectivo,
        usuario=usuario_ana,
        monto_total=5000,
        forma_pago_id=forma_pago_efectivo.id,
        usuario_id=usuario_ana.id
    )
    with pytest.raises(ValueError) as e:
        compra.validar_fecha()
    assert "fecha" in str(e.value).lower()

def test_fecha_compra_es_futura_pasa(tipo_general, forma_pago_efectivo, usuario_ana):
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo_general, tipo_entrada_id=tipo_general.id)]
    compra = Compra(
        id=4,
        fecha=date(2026, 5, 1),
        cantidad_entradas=1,
        entradas=entradas,
        forma_pago=forma_pago_efectivo,
        usuario=usuario_ana,
        monto_total=5000,
        forma_pago_id=forma_pago_efectivo.id,
        usuario_id=usuario_ana.id
    )
    assert compra.validar_fecha()

# --- FORMAS DE PAGO ---
def test_compra_con_efectivo_pasa(tipo_general, forma_pago_efectivo, usuario_luis):
    entrada = Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo_general, tipo_entrada_id=tipo_general.id)
    compra = Compra(
        id=4,
        fecha=date.today(),
        cantidad_entradas=1,
        entradas=[entrada],
        monto_total=5000,
        forma_pago=forma_pago_efectivo,
        usuario=usuario_luis,
        forma_pago_id=forma_pago_efectivo.id,
        usuario_id=usuario_luis.id
    )
    assert compra.validar_formaPago() == "Efectivo"

def test_redireccion_mercado_pago_pasa(tipo_general, forma_pago_tarjeta, usuario_luis):
    entrada = Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo_general, tipo_entrada_id=tipo_general.id)
    compra = Compra(
        id=4,
        fecha=date.today(),
        cantidad_entradas=1,
        entradas=[entrada],
        monto_total=5000,
        forma_pago=forma_pago_tarjeta,
        usuario=usuario_luis,
        forma_pago_id=forma_pago_tarjeta.id,
        usuario_id=usuario_luis.id
    )
    gateway = MercadoPagoClient()
    redirect_url = compra.obtener_redirect_pago(gateway)
    assert redirect_url.startswith("https://sandbox.mercadopago.com/checkout/v1/redirect?pref_id=MOCK_")

# --- ENVIO DE EMAIL Y MONTO TOTAL ---
def test_compra_tres_entradas_monto_y_confirmacion_pasa(tipo_general, tipo_vip, forma_pago_tarjeta, usuario_luis):
    entradas = [
        Entrada(id=1, precio_unitario=5000, edad=8, tipo_entrada=tipo_general, tipo_entrada_id=tipo_general.id),
        Entrada(id=2, precio_unitario=5000, edad=1, tipo_entrada=tipo_general, tipo_entrada_id=tipo_general.id),
        Entrada(id=3, precio_unitario=5000, edad=40, tipo_entrada=tipo_vip, tipo_entrada_id=tipo_vip.id)
    ]
    compra = Compra(
        id=4,
        fecha=date.today(),
        cantidad_entradas=3,
        entradas=entradas,
        forma_pago=forma_pago_tarjeta,
        usuario=usuario_luis,
        monto_total=0,
        forma_pago_id=forma_pago_tarjeta.id,
        usuario_id=usuario_luis.id
    )
    total_calculado = compra.calcular_monto_total()
    assert total_calculado == 12500
    assert compra.monto_total == 12500
    assert compra.validar_formaPago() == "Tarjeta"
    assert compra.enviar_confirmacion_email() is True



