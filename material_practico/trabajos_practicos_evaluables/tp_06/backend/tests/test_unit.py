import pytest
from entidades.compra import Compra
from entidades.entrada import Entrada
from entidades.tipoEntrada import TipoEntrada
from entidades.formaPago import FormaPago
from entidades.usuario import Usuario
from datetime import date

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


def test_crear_entrada_no_tiene_edad_falla():
    tipo = TipoEntrada(id=2,nombre="General")
    entrada = Entrada(id=10, precio_unitario=5000, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    with pytest.raises(ValueError):
        entrada.validar_atributos()


def test_crear_entrada_no_tiene_tipoEntrada_falla():
    entrada = Entrada(id=10, precio_unitario=5000, edad=25)
    with pytest.raises(ValueError):
        entrada.validar_atributos()


def test_crear_compra_no_tiene_entradas_falla():
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    forma_pago = FormaPago(id=1,nombre="Efectivo")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=0, monto_total=5000, forma_pago=forma_pago, usuario=usuario, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(ValueError):
        compra.validar_atributos()


def test_crear_compra_no_tiene_fecha_falla():
    tipo = TipoEntrada(id=2,nombre="General")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    forma_pago = FormaPago(id=1,nombre="Efectivo")
    compra = Compra(id=4,cantidad_entradas=1, entradas=entradas, monto_total=5000, forma_pago=forma_pago, usuario=usuario, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(ValueError):
        compra.validar_atributos()



def test_crear_compra_con_cantidad_entradas_no_coincidente_falla():
    tipo = TipoEntrada(id=2,nombre="General")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="Efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=2, entradas=entradas, forma_pago=forma_pago, usuario=usuario, monto_total=5000, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(ValueError):
        compra.validar_cantidad_entradas_coincide()


# FECHA COMPRA
def test_fecha_compra_es_menor_actual_falla():
    tipo = TipoEntrada(id=2,nombre="General")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="Efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date(2020, 3, 1), cantidad_entradas=1, entradas=entradas, forma_pago=forma_pago, usuario=usuario, monto_total=5000, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
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


def test_fecha_compra_es_dia_festivo_falla():
    tipo = TipoEntrada(id=2,nombre="General")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="Efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date(2026, 12, 25), cantidad_entradas=1, entradas=entradas, forma_pago=forma_pago, usuario=usuario, monto_total=5000, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(ValueError) as e:
        compra.validar_fecha()
    assert "fecha" in str(e.value).lower()


def test_fecha_compra_lunes_falla():
    tipo = TipoEntrada(id=2,nombre="General")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="Efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date(2026, 7, 6), cantidad_entradas=1, entradas=entradas, forma_pago=forma_pago, usuario=usuario, monto_total=5000, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(ValueError) as e:
        compra.validar_fecha()
    assert "fecha" in str(e.value).lower()


# FORMAS DE PAGO
def test_crear_compra_no_tiene_formaPago_falla():
    tipo = TipoEntrada(id=2,nombre="General")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=1, entradas=entradas, monto_total=5000, usuario=usuario, usuario_id=usuario.id)
    with pytest.raises(ValueError):
        compra.validar_atributos()


def test_compra_con_efectivo_pasa():
    tipo = TipoEntrada(id=2,nombre="General")
    formaDePago = FormaPago(id=1,nombre="Efectivo")
    entrada = Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    usuario = Usuario(id=1,nombre="Luis", apellido="Gomez", email="luis.gomez@example.com")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=1, entradas=[entrada], monto_total=5000, forma_pago=formaDePago, usuario=usuario, forma_pago_id=formaDePago.id, usuario_id=usuario.id)
    assert compra.validar_forma_pago() == "Efectivo"


def test_compra_con_tarjeta_pasa():
    tipo = TipoEntrada(id=2,nombre="General")
    formaDePago = FormaPago(id=2,nombre="Tarjeta")
    entrada = Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    usuario = Usuario(id=1,nombre="Luis", apellido="Gomez", email="luis.gomez@example.com")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=1, entradas=[entrada], monto_total=5000, forma_pago=formaDePago, usuario=usuario, forma_pago_id=formaDePago.id, usuario_id=usuario.id)
    assert compra.validar_forma_pago() == "Tarjeta"


# FORMATOS
def test_edad_decimal_falla():
    tipo = TipoEntrada(id=2,nombre="General")
    entrada = Entrada(id=1, precio_unitario=5000, edad=25.5, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    with pytest.raises(ValueError) as e:
        entrada.validar_atributos()


def test_edad_negativa_falla():
    tipo = TipoEntrada(id=2,nombre="General")
    entrada = Entrada(id=1, precio_unitario=5000, edad=-5, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    with pytest.raises(ValueError) as e:
        entrada.validar_atributos()


def test_edad_string_falla():
    tipo = TipoEntrada(id=2,nombre="General")
    entrada = Entrada(id=1, precio_unitario=5000, edad="veinte", tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    with pytest.raises((ValueError)) as e:
        entrada.validar_atributos()


def test_crear_compra_con_cantidad_entradas_decimal_falla():
    tipo = TipoEntrada(id=2,nombre="General")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="Efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=1.5, entradas=entradas, forma_pago=forma_pago, monto_total=5000, usuario=usuario, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(ValueError) as e:
        compra.validar_cantidad_entradas()
    assert "cantidad" in str(e.value).lower()


def test_crear_compra_con_cantidad_entradas_negativo_falla():
    tipo = TipoEntrada(id=2,nombre="General")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="Efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=-1, entradas=entradas, forma_pago=forma_pago, monto_total=5000, usuario=usuario, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(ValueError) as e:
        compra.validar_cantidad_entradas()
    assert "cantidad" in str(e.value).lower()


def test_crear_compra_cantidad_entradas_string_falla():
    tipo = TipoEntrada(id=2,nombre="General")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="Efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas="dos", entradas=entradas, forma_pago=forma_pago, monto_total=5000, usuario=usuario, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises((TypeError, ValueError)):
        compra.validar_cantidad_entradas()


# ENVIO DE EMAIL
def test_confirmacion_compra_enviar_mail_pasa():
    tipo = TipoEntrada(id=2,nombre="General")
    formaDePago = FormaPago(id=2,nombre="Tarjeta")
    usuario = Usuario(id=1,nombre="Luis", apellido="Gomez", email="luis@gmail.com")
    entrada = Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo)
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=1, entradas=[entrada], monto_total=5000, forma_pago=formaDePago, usuario=usuario, forma_pago_id=formaDePago.id, usuario_id=usuario.id)
    resultado = compra.enviar_confirmacion_email()
    assert resultado == True


def test_crear_compra_no_tiene_usuario_falla():
    tipo = TipoEntrada(id=2,nombre="General")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="Efectivo")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=1, entradas=entradas, forma_pago=forma_pago, monto_total=5000, forma_pago_id=forma_pago.id)
    with pytest.raises(ValueError):
        compra.validar_atributos()


def test_compra_tres_entradas_monto_y_confirmacion_pasa(
    tipo_general, tipo_vip, forma_pago_tarjeta, usuario_luis
):

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
    assert compra.validar_forma_pago() == "Tarjeta"
    assert compra.enviar_confirmacion_email() is True


def test_crear_usuario_sin_nombre_falla():
    usuario = Usuario(id=4,apellido="Gomez", email="gomez@example.com")
    with pytest.raises(ValueError):
        usuario.validar_atributos()


def test_crear_usuario_sin_email_falla():
    usuario = Usuario(id=4,nombre="Juan", apellido="Gomez")
    with pytest.raises(ValueError):
        usuario.validar_atributos()


def test_crear_usuario_sin_apellido_falla():
    usuario = Usuario(id=9,nombre="Juan", email="gomez@example.com")
    with pytest.raises(ValueError):
        usuario.validar_atributos()


def test_crear_usuario_con_todos_los_atributos_pasa():
    usuario = Usuario(id=6,nombre="Juan", apellido="Gomez", email="gomez@example.com")
    assert usuario.id == 6
    assert usuario.nombre == "Juan"
    assert usuario.apellido == "Gomez"
    assert usuario.email == "gomez@example.com"

def test_crear_tipoEntrada_sin_id_falla():
    tipo = TipoEntrada(nombre="General")
    with pytest.raises(ValueError):
        tipo.validar_atributos()

def test_crear_tipoEntrada_sin_nombre_falla():
    tipo = TipoEntrada(id=1)
    with pytest.raises(ValueError):
        tipo.validar_atributos()


def test_crear_formaPago_sin_id_falla():
    forma = FormaPago(nombre="Efectivo")
    with pytest.raises(ValueError):
        forma.validar_atributos()

def test_crear_formaPago_sin_nombre_falla():
    forma = FormaPago(id=1)
    with pytest.raises(ValueError):
        forma.validar_atributos()
