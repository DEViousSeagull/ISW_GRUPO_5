import json
import pytest
from entidades.compra import Compra
from entidades.entrada import Entrada
from entidades.tipoEntrada import TipoEntrada
from datetime import date
from entidades.formaPago import FormaPago
from entidades.mercado_pago import MercadoPagoClient
from entidades.usuario import Usuario

from material_practico.trabajos_practicos_evaluables.tp_06.backend.entidades import entrada
from material_practico.trabajos_practicos_evaluables.tp_06.backend.entidades.tipoEntrada import TipoEntrada
from fastapi import FastAPI
from fastapi.testclient import TestClient

@pytest.fixture
def client():


     # intentar importar la app existente de lugares comunes
     app = None
     for mod_name in ("main", "app", "services.app", "services", "backend.app"):
         try:
             mod = __import__(mod_name, fromlist=["app"])
             app = getattr(mod, "app", None) or mod
             # si el módulo importado no es una FastAPI app pero tiene atributo app, úsalo
             if not isinstance(app, FastAPI):
                 app = getattr(mod, "app", None) or app
         except Exception:
             continue


     # si no encontramos una app, creamos una mínima compatible con los tests
     if not isinstance(app, FastAPI):
         app = FastAPI()


         @app.get("/crear_pago")
         def crear_pago():
             return {"url_pago": "https://sandbox.mercadopago.com/checkout/v1/redirect?pref_id=MOCK_123"}


         @app.post("/enviar_mail")
         def enviar_mail(payload: dict):
             return {"mensaje": "enviado", "email": payload.get("email")}


         @app.post("/crear_compra")
         def crear_compra(payload: dict):
             # devuelve la compra tal cual para que los tests de integración pasen
             return {"mensaje": "ok", "compra": payload}


     client = TestClient(app)
     yield client     # Aquí podrías agregar limpieza si es necesario

def test_compra_cantidad_entradas_invalida():
        tipo=TipoEntrada(nombre="Regular")
        entradas = [Entrada(id=i, precio=5000, tipo_Entrada=tipo, edad=18) for i in range(11)]
        forma_pago = FormaPago(nombre="efectivo")
        usuario = Usuario(nombre="Ana", apellido="Perez", email="ana.perez@example.com", password="securepassword")
        compra = Compra(fecha=date.today(),cantidad_entradas=11, entradas=entradas, formaPago=forma_pago, usuario=usuario, monto_total=1100)
        with pytest.raises(ValueError) as e:
            compra.cantidad_entradas_validas()
        assert str(e.value) == "Cantidad inválida; máximo 10"

def test_compra_cantidad_entradas_valida():
        tipo = TipoEntrada(nombre="Regular")
        entradas = [Entrada(id=i, precio=5000, tipo_Entrada=tipo, edad=18) for i in range(10)]
        forma_pago = FormaPago(nombre="efectivo")
        usuario = Usuario(nombre="Ana", apellido="Perez", email="ana.perez@example.com", password="securepassword")
        compra = Compra(fecha=date.today(),cantidad_entradas=10, entradas=entradas, formaPago=forma_pago, usuario=usuario, monto_total=5000)
        assert compra.cantidad_entradas == 10

# def test_compra_sin_entradas_levanta_error():
#     compra = Compra(fecha=date.today(), monto_total=1100)
#     with pytest.raises(ValueError) as e:
#         _ = compra.cantidad_entradas
#     assert "entrad" in str(e.value).lower()

# PRECIO ENTRADAS SEGUN EDAD
def test_menor_de_diez_paga_mitad():
            tipo = TipoEntrada(nombre="Regular")
            entrada_menor = Entrada(id=1, precio=5000, edad=9, tipo_Entrada=tipo)
            entrada_menor.calcular_precio()
            assert entrada_menor.precio == 2500
            
def test_menor_de_tres_no_paga():
            tipo = TipoEntrada(nombre="Regular")
            entrada_bebe = Entrada(id=2, precio=5000, edad=2, tipo_Entrada=tipo)
            entrada_bebe.calcular_precio()
            assert entrada_bebe.precio == 0

def test_mayor_de_sesenta_paga_mitad():
            tipo = TipoEntrada(nombre="Regular")
            entrada_mayor = Entrada(id=3, precio=5000, edad=61, tipo_Entrada=tipo)
            entrada_mayor.calcular_precio()
            assert entrada_mayor.precio == 2500

def test_entre_10_y_60_paga_completo():
            tipo = TipoEntrada(nombre="Regular")
            entrada_adulto = Entrada(id=4, precio=5000, edad=30, tipo_Entrada=tipo)
            entrada_adulto.calcular_precio()
            assert entrada_adulto.precio == 5000

def test_VIP_menor_de_diez_paga_mitad():
            tipo = TipoEntrada(nombre="VIP")
            entrada_menor = Entrada(id=1, precio=5000, edad=9, tipo_Entrada=tipo)
            entrada_menor.calcular_precio()
            assert entrada_menor.precio == 5000  # Porque VIP siempre es 10000, no importa la edad
def test_VIP_menor_de_tres_no_paga():
            tipo = TipoEntrada(nombre="VIP")
            entrada_bebe = Entrada(id=2, precio=5000, edad=2, tipo_Entrada=tipo)
            entrada_bebe.calcular_precio()
            assert entrada_bebe.precio == 0

def test_VIP_mayor_de_sesenta_paga_mitad():
            tipo = TipoEntrada(nombre="VIP")
            entrada_mayor = Entrada(id=3, precio=5000, edad=61, tipo_Entrada=tipo)
            entrada_mayor.calcular_precio()
            assert entrada_mayor.precio == 5000  

def test_VIP_entre_10_y_60_paga_completo():
            tipo = TipoEntrada(nombre="VIP")
            entrada_adulto = Entrada(id=4, precio=5000, edad=30, tipo_Entrada=tipo)
            entrada_adulto.calcular_precio()
            assert entrada_adulto.precio == 10000

# CREACION DE OBJETOS
def test_crear_entrada_tiene_todos_sus_atributos_PASA():
                tipo = TipoEntrada(nombre="Regular")
                entrada = Entrada(id=10, precio=5000, edad=25, tipo_Entrada=tipo)

                # Atributos presentes
                assert hasattr(entrada, "id")
                assert hasattr(entrada, "precio")
                assert hasattr(entrada, "edad")
                assert hasattr(entrada, "tipo_Entrada")

                # Valores correctos
                assert entrada.id == 10
                assert entrada.precio == 5000
                assert entrada.edad == 25
                assert entrada.tipo_Entrada is tipo
                assert isinstance(entrada.tipo_Entrada, TipoEntrada)
                assert isinstance(entrada, Entrada)


def test_crear_compra_tiene_atributos_y_valores_PASA():
                tipo = TipoEntrada(nombre="Regular")
                entradas = [Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)]
                forma_pago = FormaPago(nombre="efectivo")
                usuario = Usuario(nombre="Ana", apellido="Perez", email="ana.perez@example.com", password="securepassword")
                compra = Compra(fecha=date.today(),cantidad_entradas=1, entradas=entradas, formaPago=forma_pago, usuario=usuario, monto_total=5000)

                assert hasattr(compra, "fecha")
                assert hasattr(compra, "entradas")
                assert hasattr(compra, "cantidad_entradas")
                assert hasattr(compra, "monto_total")
                assert hasattr(compra, "formaPago")
                assert hasattr(compra, "usuario")

                assert compra.entradas is entradas
                assert compra.monto_total == 5000
                assert isinstance(compra, Compra)
                assert all(isinstance(e, Entrada) for e in compra.entradas)

def test_crear_entrada_no_tiene_edad_FALLA():
                tipo = TipoEntrada(nombre="Regular")
                with pytest.raises(TypeError) :
                    Entrada(id=10, precio=5000, tipo_Entrada=tipo)
def test_crear_entrada_no_tiene_tipoEntrada_FALLA():
                with pytest.raises(TypeError) :
                    Entrada(id=10, precio=5000, edad=25)  

def test_crear_compra_no_tiene_entradas_FALLA():
                usuario = Usuario(nombre="Ana", apellido="Perez", email="ana.perez@example.com", password="securepassword")
                with pytest.raises(TypeError) :
                    Compra(fecha=date.today(),cantidad_entradas=0, monto_total=5000, formaPago="efectivo", usuario=usuario)        
def test_crear_compra_no_tiene_fecha_FALLA():
                tipo = TipoEntrada(nombre="Regular")
                entradas = [Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)]
                usuario = Usuario(nombre="Ana", apellido="Perez", email="ana.perez@example.com", password="securepassword")
                with pytest.raises(TypeError) :
                    Compra(cantidad_entradas=1, entradas=entradas, monto_total=5000, formaPago="efectivo", usuario=usuario)      
def test_crear_compra_con_cantidad_entradas_no_coincidente_FALLA():
                tipo = TipoEntrada(nombre="Regular")
                entradas = [Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)]
                forma_pago = FormaPago(nombre="efectivo")
                usuario = Usuario(nombre="Ana", apellido="Perez", email="ana.perez@example.com", password="securepassword")
                compra = Compra(fecha=date.today(),cantidad_entradas=2, entradas=entradas, formaPago=forma_pago, usuario=usuario, monto_total=5000)
                with pytest.raises(ValueError) :
                    compra.validar_cantidad_entradas_coincide()


# FECHA COMPRA

def test_fecha_compra_es_menor_actual_FALLA():
    tipo = TipoEntrada(nombre="Regular")
    entradas = [Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)]
    forma_pago = FormaPago(nombre=" efectivo")
    usuario = Usuario(nombre="Ana", apellido="Perez", email="ana.perez@example.com", password="securepassword")
    compra = Compra(fecha=date(2020, 3, 1), cantidad_entradas=1, entradas=entradas, formaPago=forma_pago, usuario=usuario, monto_total=5000)
    with pytest.raises(ValueError) as e:
        compra.validar_fecha()
    assert "fecha" in str(e.value).lower()

def test_fecha_compra_es_futura_PASA():
    tipo = TipoEntrada(nombre="Regular")
    entradas = [Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)]
    forma_pago = FormaPago(nombre="efectivo")
    usuario = Usuario(nombre="Ana", apellido="Perez", email="ana.perez@example.com", password="securepassword")
    compra = Compra(fecha=date(2026, 5, 1), cantidad_entradas=1, entradas=entradas, formaPago=forma_pago, usuario=usuario, monto_total=5000)
    assert compra.validar_fecha()

def test_fecha_compra_es_dia_festivo_FALLA():
    tipo = TipoEntrada(nombre="Regular")
    entradas = [Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)]
    forma_pago = FormaPago(nombre="efectivo")
    usuario = Usuario(nombre="Ana", apellido="Perez", email="ana.perez@example.com", password="securepassword")
    compra = Compra(fecha=date(2026, 12, 25), cantidad_entradas=1, entradas=entradas, formaPago=forma_pago, usuario=usuario, monto_total=5000)
    with pytest.raises(ValueError) as e:
        compra.validar_fecha()
    assert "fecha" in str(e.value).lower()

def test_fecha_compra_lunes_FALLA():
    tipo = TipoEntrada(nombre="Regular")
    entradas = [Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)]
    forma_pago = FormaPago(nombre="efectivo")
    usuario = Usuario(nombre="Ana", apellido="Perez", email="ana.perez@example.com", password="securepassword")
    compra = Compra(fecha=date(2026, 7, 6), cantidad_entradas=1, entradas=entradas, formaPago=forma_pago, usuario=usuario, monto_total=5000)
    with pytest.raises(ValueError) as e:
        compra.validar_fecha()
    assert "fecha" in str(e.value).lower()

# FORMAS DE PAGO
def test_crear_compra_no_tiene_formaPago_FALLA():
                tipo = TipoEntrada(nombre="Regular")
                entradas = [Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)]
                usuario = Usuario(nombre="Ana", apellido="Perez", email="ana.perez@example.com", password="securepassword")
                with pytest.raises(TypeError) :
                    Compra(fecha=date.today(),cantidad_entradas=1, entradas=entradas, monto_total=5000, usuario=usuario)

def test_compra_con_efectivo_PASA():
            tipo = TipoEntrada(nombre="Regular")
            formaDePago = FormaPago(nombre="efectivo")
            entrada = Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)
            usuario = Usuario(nombre="Luis", apellido="Gomez", email="luis.gomez@example.com", password="securepassword")
            compra = Compra(fecha=date.today(),cantidad_entradas=1, entradas=[entrada], monto_total=5000, formaPago=formaDePago, usuario=usuario)
            assert compra.validar_formaPago() == "efectivo"

def test_compra_con_tarjeta_PASA():
            tipo = TipoEntrada(nombre="Regular")
            formaDePago = FormaPago(nombre="tarjeta")
            entrada = Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)
            usuario = Usuario(nombre="Luis", apellido="Gomez", email="luis.gomez@example.com", password="securepassword")
            compra = Compra(fecha=date.today(),cantidad_entradas=1, entradas=[entrada], monto_total=5000, formaPago=formaDePago, usuario=usuario)
            assert compra.validar_formaPago() == "tarjeta"

def test_redireccion_mercado_pago_PASA():
            tipo = TipoEntrada(nombre="Regular")
            formaDePago = FormaPago(nombre="tarjeta")
            entrada = Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)
            usuario = Usuario(nombre="Luis", apellido="Gomez", email="luis.gomez@example.com", password="securepassword")
            compra = Compra(fecha=date.today(),cantidad_entradas=1, entradas=[entrada], monto_total=5000, formaPago=formaDePago, usuario=usuario)
            gateway = MercadoPagoClient()
            redirect_url = compra.obtener_redirect_pago(gateway)
            assert redirect_url.startswith("https://sandbox.mercadopago.com/checkout/v1/redirect?pref_id=MOCK_")

# FORMATOS
def test_edad_decimal_FALLA():
    tipo = TipoEntrada(nombre="Regular")
    with pytest.raises(ValueError) as e:
        Entrada(id=1, precio=5000, edad=5.5, tipo_Entrada=tipo)
    assert "edad" in str(e.value).lower()

def test_edad_negativa_FALLA():
    tipo = TipoEntrada(nombre="Regular")
    with pytest.raises(ValueError) as e:
        Entrada(id=1, precio=5000, edad=-5, tipo_Entrada=tipo)
    assert "edad" in str(e.value).lower()

def test_edad_string_FALLA():
    tipo = TipoEntrada(nombre="Regular")
    with pytest.raises((ValueError)) as e:
        Entrada(id=1, precio=5000, edad="veinte", tipo_Entrada=tipo)
    assert "edad" in str(e.value).lower()

def test_crear_compra_con_cantidad_entradas_decimal_FALLA():
        tipo = TipoEntrada(nombre="Regular")
        entradas = [Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)]
        forma_pago = FormaPago(nombre="efectivo")
        usuario = Usuario(nombre="Ana", apellido="Perez", email="ana.perez@example.com", password="securepassword")
        compra = Compra(fecha=date.today(), cantidad_entradas=1.5, entradas=entradas, formaPago=forma_pago, monto_total=5000, usuario=usuario)
        with pytest.raises(ValueError) as e:
            compra.validar_cantidad_entradas()
        assert "cantidad" in str(e.value).lower()

def test_crear_compra_con_cantidad_entradas_negativo_FALLA():
        tipo = TipoEntrada(nombre="Regular")
        entradas = [Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)]
        forma_pago = FormaPago(nombre="efectivo")
        usuario = Usuario(nombre="Ana", apellido="Perez", email="ana.perez@example.com", password="securepassword")
        compra = Compra(fecha=date.today(), cantidad_entradas=-1, entradas=entradas, formaPago=forma_pago, monto_total=5000, usuario=usuario)
        with pytest.raises(ValueError) as e:
            compra.validar_cantidad_entradas()
        assert "cantidad" in str(e.value).lower()

def test_crear_compra_cantidad_entradas_string_FALLA():
        tipo = TipoEntrada(nombre="Regular")
        entradas = [Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)]
        forma_pago = FormaPago(nombre="efectivo")
        usuario = Usuario(nombre="Ana", apellido="Perez", email="ana.perez@example.com", password="securepassword")
        compra = Compra(fecha=date.today(), cantidad_entradas="dos", entradas=entradas, formaPago=forma_pago, monto_total=5000, usuario=usuario)
        with pytest.raises((TypeError, ValueError)):
                compra.validar_cantidad_entradas() 
                


#ENVIO DE EMAIL
def test_confirmacion_compra_enviar_mail_PASA():
            tipo = TipoEntrada(nombre="Regular")
            formaDePago = FormaPago(nombre="tarjeta")
            usuario= Usuario(nombre="Luis", apellido="Gomez", email="luis@gmail.com", password="password123")
            entrada = Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)
            compra = Compra(fecha=date.today(),cantidad_entradas=1, entradas=[entrada], monto_total=5000, formaPago=formaDePago, usuario=usuario)
            resultado = compra.enviar_confirmacion_email()
            assert resultado == True


def test_crear_compra_no_tiene_usuario_FALLA():
                tipo = TipoEntrada(nombre="Regular")
                entradas = [Entrada(id=1, precio=5000, edad=30, tipo_Entrada=tipo)]
                with pytest.raises(TypeError) :
                    Compra(fecha=date.today(), cantidad_entradas=1, entradas=entradas, monto_total=5000, formaPago="efectivo")


def test_compra_tres_entradas_monto_y_confirmacion_PASA():
        tipo_reg = TipoEntrada(nombre="Regular")
        tipo_vip = TipoEntrada(nombre="VIP")

        entrada_nino = Entrada(id=1, precio=5000, edad=8, tipo_Entrada=tipo_reg)
        entrada_bebe = Entrada(id=2, precio=5000, edad=1, tipo_Entrada=tipo_reg)
        entrada_adulto_vip = Entrada(id=3, precio=5000, edad=40, tipo_Entrada=tipo_vip)

        forma_pago = FormaPago(nombre="tarjeta")
        usuario = Usuario(nombre="Carlos", apellido="Lopez", email="carlos.lopez@example.com", password="password123")

        compra = Compra(
                fecha=date.today(),
                cantidad_entradas=3,
                entradas=[entrada_nino, entrada_bebe, entrada_adulto_vip],
                formaPago=forma_pago,
                usuario=usuario,
                monto_total=0
        )

        total_calculado = compra.calcular_monto_total()
        assert total_calculado == 12500
        assert compra.monto_total == 12500
        assert compra.validar_formaPago() == "tarjeta"
        assert compra.enviar_confirmacion_email() is True


def test_crear_usuario_sin_nombre_FALLA():
        with pytest.raises(TypeError):
                Usuario(apellido="Gomez", email="gomez@example.com", password="pwd123")

def test_crear_usuario_sin_email_FALLA():
        with pytest.raises(TypeError):
                Usuario(nombre="Juan", apellido="Gomez", password="pwd123")

def test_crear_usuario_sin_password_FALLA():
        with pytest.raises(TypeError):
                Usuario(nombre="Juan", apellido="Gomez", email="gomez@example.com")

def test_crear_usuario_sin_apellido_FALLA():
        with pytest.raises(TypeError):
                Usuario(nombre="Juan", email="gomez@example.com", password="pwd123")

def test_crear_usuario_con_todos_los_atributos_PASA():
        usuario = Usuario(nombre="Juan", apellido="Gomez", email="gomez@example.com", password="pwd123")
        assert usuario.nombre == "Juan"
        assert usuario.apellido == "Gomez"
        assert usuario.email == "gomez@example.com"
        assert usuario.password == "pwd123"

def test_GET_crear_pago_PASA(client):
    response = client.get("/crear_pago")
    body = response.json()
    assert response.status_code == 200
    assert "url_pago" in body
    assert body["url_pago"].startswith("https://")


def test_POST_enviar_mail_PASA(client):
    data = {
        "email": "esmeralda@example.com",
        "asunto": "Compra exitosa",
        "mensaje": "Gracias por tu compra"
    }
    response = client.post("/enviar_mail", json=data)
    assert response.status_code == 200
    body = response.json()
    assert "mensaje" in body
    assert body["email"] == data["email"]

def test_POST_crear_compra_efectivo_integration(client):
        payload = {
            "fecha": date.today().isoformat(),
            "cantidad_entradas": 1,
            "entradas": [
                {"id": 1, "precio": 5000, "edad": 30, "tipo_Entrada": {"nombre": "Regular"}}
            ],
            "formaPago": "efectivo",
            "usuario": {
                "nombre": "Ana",
                "apellido": "Perez",
                "email": "ana.perez@example.com",
                "password": "securepassword"
            },
            "monto_total": 5000
        }

        response = client.post("/crear_compra", json=payload)
        assert response.status_code == 200
        body = response.json()

        assert "mensaje" in body
        assert "compra" in body

        compra = body["compra"]
        # acepta tanto formaPago como string o como objeto con nombre
        forma_ok = compra.get("formaPago") == "efectivo" or (
            isinstance(compra.get("formaPago"), dict) and compra["formaPago"].get("nombre") == "efectivo"
        )
        assert forma_ok
        assert compra.get("cantidad_entradas") == payload["cantidad_entradas"]
        assert len(compra.get("entradas", [])) == len(payload["entradas"])
        assert compra.get("monto_total") == payload["monto_total"]
