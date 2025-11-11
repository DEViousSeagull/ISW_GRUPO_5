import pytest
import sys, os
from fastapi.testclient import TestClient
from datetime import date


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main import app  

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


#TEST FORMAS DE PAGO
def test_get_formas_de_pago_efectivo_pasa(client):
    response = client.get("/formas_pago")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert any(fp.get("nombre") == "Efectivo" for fp in body)

#TEST TIPOS DE ENTRADA
def test_get_tipos_de_entrada_general_pasa(client):
    response = client.get("/tipos_entrada")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert any(te.get("nombre") == "General" for te in body)

def test_get_tipos_de_entrada_vip_pasa(client):
    response = client.get("/tipos_entrada")
    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert any(te.get("nombre") == "VIP" for te in body)

def test_post_crear_compra_efectivo_pasa(client):
        payload = {
        "fecha": "2025-10-23",
        "cantidad_entradas": 1,
        "monto_total": 10000,
        "forma_pago": {"id": 1, "nombre": "Efectivo"},
        "usuario": {
            "id": 1,
            "nombre": "Ana",
            "apellido": "Gómez",
            "email": "ana.gomez@example.com",
        },
        "entradas": [
            {
                "id": 999,
                "precio_unitario": 10000,
                "edad": 25,
                "tipo_entrada": {"id": 1, "nombre": "VIP"}
            }
        ]     
     }

        response = client.post("/compras/crear_compra", json=payload)
        assert response.status_code == 200
        body = response.json()

        assert "mensaje" in body
        assert "compra" in body

        compra = body["compra"]

        #assert compra["usuario"]["email"] == payload["usuario"]["email"]
        assert compra["forma_pago"]["nombre"] == payload["forma_pago"]["nombre"]
        #assert compra["monto_total"] == payload["monto_total"]

def test_get_compras_pasa(client):
    # Solicitar lista de compras
    response = client.get("/compras", params={"page": 1, "pageSize": 50})
    
    # Verificar respuesta exitosa
    assert response.status_code == 200
    
    # Obtener body de la respuesta
    body = response.json()
    
    # Manejar tanto respuesta como lista directa o dentro de "Items"
    items = body.get("Items") if isinstance(body, dict) and "Items" in body else body
    
    # Verificar que es una lista
    assert isinstance(items, list)
    
    # Verificar que cada item tiene la estructura esperada
    item = items[0]

    assert isinstance(item, dict)
    assert "id" in item
    assert "fecha" in item
    assert "cantidad_entradas" in item
    assert "monto_total" in item
    assert "forma_pago" in item
    assert "usuario" in item
    assert len(item["entradas"]) == item["cantidad_entradas"]


    # Verificar que los datos de la compra sean los esperado
    # assert item["id"] == 1
    # assert item["fecha"] == date.today().isoformat()
    # assert item["cantidad_entradas"] == 1
    # assert len(item["entradas"]) == 1
    # assert item["entradas"][0]["id"] == 1
    # assert item["entradas"][0]["precio_unitario"] == 5000
    # assert item["entradas"][0]["edad"] == 30
    # assert item["entradas"][0]["tipo_entrada"]["nombre"] == "General"
    # assert item["forma_pago"]["id"] == 1
    # assert item["usuario"]["nombre"] == "Juan"
    # assert item["usuario"]["apellido"] == "Pérez"
    # assert item["usuario"]["email"] == "juan@example.com"
    # assert item["usuario"]["id"] == 1
    # assert item["monto_total"] == 5000

