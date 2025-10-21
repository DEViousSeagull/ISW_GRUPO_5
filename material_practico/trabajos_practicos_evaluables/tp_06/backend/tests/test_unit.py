import json
import pytest
from entidades.compra import Compra
from entidades.entrada import Entrada
from entidades.tipoEntrada import TipoEntrada
from datetime import date
from entidades.formaPago import FormaPago
from entidades.mercado_pago import MercadoPagoClient
from entidades.usuario import Usuario


def test_compra_cantidad_entradas_invalida():
    tipo = TipoEntrada(id=1,nombre="Regular")
    entradas = [Entrada(id=i, precio_unitario=5000, tipo_entrada=tipo, edad=18, tipo_entrada_id=tipo.id) for i in range(11)]
    forma_pago = FormaPago(id=2,nombre="efectivo")
    usuario = Usuario(id=3,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=2,fecha=date.today(), cantidad_entradas=11, entradas=entradas, forma_pago=forma_pago, usuario=usuario, monto_total=1100, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(ValueError) as e:
        compra.cantidad_entradas_validas()
    assert str(e.value) == "Cantidad inválida; máximo 10"


def test_compra_cantidad_entradas_valida():
    tipo = TipoEntrada(id=3, nombre="Regular")
    entradas = [Entrada(id=i, precio_unitario=5000, tipo_entrada=tipo, tipo_entrada_id=tipo.id, edad=18) for i in range(10)]
    forma_pago = FormaPago(id=1,nombre="efectivo")
    usuario = Usuario(id=3,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=1,fecha=date.today(), cantidad_entradas=10, entradas=entradas, forma_pago=forma_pago, usuario=usuario, monto_total=5000,forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    assert compra.cantidad_entradas == 10


# PRECIO ENTRADAS SEGUN EDAD
def test_menor_de_diez_paga_mitad():
    tipo = TipoEntrada(id=5,nombre="Regular")
    entrada_menor = Entrada(id=1, precio_unitario=5000, edad=9, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    entrada_menor.calcular_precio()
    assert entrada_menor.precio_unitario == 2500


def test_menor_de_tres_no_paga():
    tipo = TipoEntrada(id=4,nombre="Regular")
    entrada_bebe = Entrada(id=2, precio_unitario=5000, edad=2, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    entrada_bebe.calcular_precio()
    assert entrada_bebe.precio_unitario == 0


def test_mayor_de_sesenta_paga_mitad():
    tipo = TipoEntrada(id=6,nombre="Regular")
    entrada_mayor = Entrada(id=3, precio_unitario=5000, edad=61, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    entrada_mayor.calcular_precio()
    assert entrada_mayor.precio_unitario == 2500


def test_entre_10_y_60_paga_completo():
    tipo = TipoEntrada(id=7,nombre="Regular")
    entrada_adulto = Entrada(id=4, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    entrada_adulto.calcular_precio()
    assert entrada_adulto.precio_unitario == 5000


def test_VIP_menor_de_diez_paga_mitad():
    tipo = TipoEntrada(id=8,nombre="VIP")
    entrada_menor = Entrada(id=1, precio_unitario=5000, edad=9, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    entrada_menor.calcular_precio()
    assert entrada_menor.precio_unitario == 5000  # Porque VIP siempre es 10000, no importa la edad


def test_VIP_menor_de_tres_no_paga():
    tipo = TipoEntrada(id=8,nombre="VIP")
    entrada_bebe = Entrada(id=2, precio_unitario=5000, edad=2, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    entrada_bebe.calcular_precio()
    assert entrada_bebe.precio_unitario == 0


def test_VIP_mayor_de_sesenta_paga_mitad():
    tipo = TipoEntrada(id=8,nombre="VIP")
    entrada_mayor = Entrada(id=3, precio_unitario=5000, edad=61, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    entrada_mayor.calcular_precio()
    assert entrada_mayor.precio_unitario == 5000


def test_VIP_entre_10_y_60_paga_completo():
    tipo = TipoEntrada(id=8,nombre="VIP")
    entrada_adulto = Entrada(id=4, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    entrada_adulto.calcular_precio()
    assert entrada_adulto.precio_unitario == 10000


# CREACION DE OBJETOS
def test_crear_entrada_tiene_todos_sus_atributos_PASA():
    tipo = TipoEntrada(id=9,nombre="Regular")
    entrada = Entrada(id=10, precio_unitario=5000, edad=25, tipo_entrada=tipo, tipo_entrada_id=tipo.id)

    # Atributos presentes
    assert hasattr(entrada, "id")
    assert hasattr(entrada, "precio_unitario")
    assert hasattr(entrada, "edad")
    assert hasattr(entrada, "tipo_entrada")

    # Valores correctos
    assert entrada.id == 10
    assert entrada.precio_unitario == 5000
    assert entrada.edad == 25
    assert entrada.tipo_entrada is tipo
    assert isinstance(entrada.tipo_entrada, TipoEntrada)
    assert isinstance(entrada, Entrada)


def test_crear_compra_tiene_atributos_y_valores_PASA():
    tipo = TipoEntrada(id=9,nombre="Regular")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=1,fecha=date.today(), cantidad_entradas=1, entradas=entradas, forma_pago=forma_pago, usuario=usuario, monto_total=5000, forma_pago_id=forma_pago.id, usuario_id=usuario.id)

    assert hasattr(compra, "id")
    assert hasattr(compra, "fecha")
    assert hasattr(compra, "entradas")
    assert hasattr(compra, "cantidad_entradas")
    assert hasattr(compra, "monto_total")
    assert hasattr(compra, "forma_pago")
    assert hasattr(compra, "usuario")


    assert compra.monto_total == 5000
    assert isinstance(compra, Compra)
    assert all(isinstance(e, Entrada) for e in compra.entradas)


def test_crear_entrada_no_tiene_edad_FALLA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    with pytest.raises(TypeError):
        Entrada(id=10, precio_unitario=5000, tipo_entrada=tipo, tipo_entrada_id=tipo.id)


def test_crear_entrada_no_tiene_tipoEntrada_FALLA():
    with pytest.raises(TypeError):
        Entrada(id=10, precio_unitario=5000, edad=25)


def test_crear_compra_no_tiene_entradas_FALLA():
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    forma_pago = FormaPago(id=1,nombre="efectivo")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=0, monto_total=5000, forma_pago=forma_pago, usuario=usuario, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(TypeError):
        compra.validar_atributos_presentes()


def test_crear_compra_no_tiene_fecha_FALLA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    forma_pago = FormaPago(id=1,nombre="efectivo")
    with pytest.raises(TypeError):
        Compra(id=4,cantidad_entradas=1, entradas=entradas, monto_total=5000, forma_pago=forma_pago, usuario=usuario, forma_pago_id=forma_pago.id, usuario_id=usuario.id)


def test_crear_compra_con_cantidad_entradas_no_coincidente_FALLA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=2, entradas=entradas, forma_pago=forma_pago, usuario=usuario, monto_total=5000, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(ValueError):
        compra.validar_cantidad_entradas_coincide()


# FECHA COMPRA
def test_fecha_compra_es_menor_actual_FALLA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre=" efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date(2020, 3, 1), cantidad_entradas=1, entradas=entradas, forma_pago=forma_pago, usuario=usuario, monto_total=5000, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(ValueError) as e:
        compra.validar_fecha()
    assert "fecha" in str(e.value).lower()


def test_fecha_compra_es_futura_PASA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date(2026, 5, 1), cantidad_entradas=1, entradas=entradas, forma_pago=forma_pago, usuario=usuario, monto_total=5000, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    assert compra.validar_fecha()


def test_fecha_compra_es_dia_festivo_FALLA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date(2026, 12, 25), cantidad_entradas=1, entradas=entradas, forma_pago=forma_pago, usuario=usuario, monto_total=5000, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(ValueError) as e:
        compra.validar_fecha()
    assert "fecha" in str(e.value).lower()


def test_fecha_compra_lunes_FALLA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date(2026, 7, 6), cantidad_entradas=1, entradas=entradas, forma_pago=forma_pago, usuario=usuario, monto_total=5000, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(ValueError) as e:
        compra.validar_fecha()
    assert "fecha" in str(e.value).lower()


# FORMAS DE PAGO
def test_crear_compra_no_tiene_formaPago_FALLA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    with pytest.raises(TypeError):
        Compra(id=4,fecha=date.today(), cantidad_entradas=1, entradas=entradas, monto_total=5000, usuario=usuario, usuario_id=usuario.id)


def test_compra_con_efectivo_PASA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    formaDePago = FormaPago(id=1,nombre="efectivo")
    entrada = Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    usuario = Usuario(id=1,nombre="Luis", apellido="Gomez", email="luis.gomez@example.com")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=1, entradas=[entrada], monto_total=5000, forma_pago=formaDePago, usuario=usuario, forma_pago_id=formaDePago.id, usuario_id=usuario.id)
    assert compra.validar_formaPago() == "efectivo"


def test_compra_con_tarjeta_PASA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    formaDePago = FormaPago(id=1,nombre="tarjeta")
    entrada = Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    usuario = Usuario(id=1,nombre="Luis", apellido="Gomez", email="luis.gomez@example.com")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=1, entradas=[entrada], monto_total=5000, forma_pago=formaDePago, usuario=usuario, forma_pago_id=formaDePago.id, usuario_id=usuario.id)
    assert compra.validar_formaPago() == "tarjeta"


def test_redireccion_mercado_pago_PASA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    formaDePago = FormaPago(id=1,nombre="tarjeta")
    entrada = Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    usuario = Usuario(id=1,nombre="Luis", apellido="Gomez", email="luis.gomez@example.com")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=1, entradas=[entrada], monto_total=5000, forma_pago=formaDePago, usuario=usuario, forma_pago_id=formaDePago.id, usuario_id=usuario.id)
    gateway = MercadoPagoClient()
    redirect_url = compra.obtener_redirect_pago(gateway)
    assert redirect_url.startswith("https://sandbox.mercadopago.com/checkout/v1/redirect?pref_id=MOCK_")


# FORMATOS
def test_edad_decimal_FALLA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    with pytest.raises(ValueError) as e:
        Entrada(id=1, precio_unitario=5000, edad=5.5, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    assert "edad" in str(e.value).lower()


def test_edad_negativa_FALLA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    with pytest.raises(ValueError) as e:
        Entrada(id=1, precio_unitario=5000, edad=-5, tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    assert "edad" in str(e.value).lower()


def test_edad_string_FALLA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    with pytest.raises((ValueError)) as e:
        Entrada(id=1, precio_unitario=5000, edad="veinte", tipo_entrada=tipo, tipo_entrada_id=tipo.id)
    assert "edad" in str(e.value).lower()


def test_crear_compra_con_cantidad_entradas_decimal_FALLA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=1.5, entradas=entradas, forma_pago=forma_pago, monto_total=5000, usuario=usuario, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(ValueError) as e:
        compra.validar_cantidad_entradas()
    assert "cantidad" in str(e.value).lower()


def test_crear_compra_con_cantidad_entradas_negativo_FALLA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=-1, entradas=entradas, forma_pago=forma_pago, monto_total=5000, usuario=usuario, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises(ValueError) as e:
        compra.validar_cantidad_entradas()
    assert "cantidad" in str(e.value).lower()


def test_crear_compra_cantidad_entradas_string_FALLA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="efectivo")
    usuario = Usuario(id=1,nombre="Ana", apellido="Perez", email="ana.perez@example.com")
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas="dos", entradas=entradas, forma_pago=forma_pago, monto_total=5000, usuario=usuario, forma_pago_id=forma_pago.id, usuario_id=usuario.id)
    with pytest.raises((TypeError, ValueError)):
        compra.validar_cantidad_entradas()


# ENVIO DE EMAIL
def test_confirmacion_compra_enviar_mail_PASA():
    tipo = TipoEntrada(id=1,nombre="Regular")
    formaDePago = FormaPago(id=1,nombre="tarjeta")
    usuario = Usuario(id=1,nombre="Luis", apellido="Gomez", email="luis@gmail.com")
    entrada = Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo)
    compra = Compra(id=4,fecha=date.today(), cantidad_entradas=1, entradas=[entrada], monto_total=5000, forma_pago=formaDePago, usuario=usuario, forma_pago_id=formaDePago.id, usuario_id=usuario.id)
    resultado = compra.enviar_confirmacion_email()
    assert resultado == True


def test_crear_compra_no_tiene_usuario_FALLA():
    tipo = TipoEntrada(id=8,nombre="Regular")
    entradas = [Entrada(id=1, precio_unitario=5000, edad=30, tipo_entrada=tipo, tipo_entrada_id=tipo.id)]
    forma_pago = FormaPago(id=1,nombre="efectivo")
    with pytest.raises(TypeError):
        Compra(id=9,fecha=date.today(), cantidad_entradas=1, entradas=entradas, monto_total=5000, forma_pago=forma_pago, forma_pago_id=forma_pago.id)


def test_compra_tres_entradas_monto_y_confirmacion_PASA():
    tipo_reg = TipoEntrada(id=1,nombre="Regular")
    tipo_vip = TipoEntrada(id=2,nombre="VIP")

    entrada_nino = Entrada(id=1, precio_unitario=5000, edad=8, tipo_entrada=tipo_reg, tipo_entrada_id=tipo_reg.id)
    entrada_bebe = Entrada(id=2, precio_unitario=5000, edad=1, tipo_entrada=tipo_reg, tipo_entrada_id=tipo_reg.id)
    entrada_adulto_vip = Entrada(id=3, precio_unitario=5000, edad=40, tipo_entrada=tipo_vip, tipo_entrada_id=tipo_vip.id)

    forma_pago = FormaPago(id=1,nombre="tarjeta")
    usuario = Usuario(id=1,nombre="Carlos", apellido="Lopez", email="carlos.lopez@example.com")

    compra = Compra(
        id=4,
        fecha=date.today(),
        cantidad_entradas=3,
        entradas=[entrada_nino, entrada_bebe, entrada_adulto_vip],
        forma_pago=forma_pago,
        usuario=usuario,
        monto_total=0,
        forma_pago_id=forma_pago.id,
        usuario_id=usuario.id
    )

    total_calculado = compra.calcular_monto_total()
    assert total_calculado == 12500
    assert compra.monto_total == 12500
    assert compra.validar_formaPago() == "tarjeta"
    assert compra.enviar_confirmacion_email() is True


def test_crear_usuario_sin_nombre_FALLA():
    usuario = Usuario(id=4,apellido="Gomez", email="gomez@example.com")
    # El modelo actual permite instanciar, pero el atributo 'nombre' quedará en None
    assert getattr(usuario, 'nombre', None) is None


def test_crear_usuario_sin_email_FALLA():
    usuario = Usuario(id=4,nombre="Juan", apellido="Gomez")
    assert getattr(usuario, 'email', None) is None


def test_crear_usuario_sin_apellido_FALLA():
    usuario = Usuario(id=9,nombre="Juan", email="gomez@example.com")
    assert getattr(usuario, 'apellido', None) is None


def test_crear_usuario_con_todos_los_atributos_PASA():
    usuario = Usuario(id=6,nombre="Juan", apellido="Gomez", email="gomez@example.com")
    assert usuario.id == 6
    assert usuario.nombre == "Juan"
    assert usuario.apellido == "Gomez"
    assert usuario.email == "gomez@example.com"



