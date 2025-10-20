
import sqlite3
from pathlib import Path

DB = Path("EcoHarmonyPark.db")

DDL = "schema.sql"

def init_db():
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON;")
    with open(DDL, "r") as f:
        con.executescript(f.read())

    # Semillas básicas
    con.execute("INSERT OR IGNORE INTO formas_pago (id, nombre) VALUES (1,'efectivo'), (2,'tarjeta');")
    con.execute("""
        INSERT OR IGNORE INTO usuarios (id, nombre, apellido, email)
        VALUES (1, 'Juan', 'Pérez', 'juan@example.com');
    """)
    # Entradas ejemplo
    con.execute("""
        INSERT OR IGNORE INTO entradas (id, edad, tipo, precio_unitario)
        VALUES (100, 30, 'regular', 10000.0),
               (101, 12, 'menor',   7000.0);
    """)
    con.commit()
    con.close()

def crear_compra(fecha:str, cantidad:int, forma_pago_id:int, usuario_id:int):
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON;")
    cur = con.cursor()
    cur.execute("""
        INSERT INTO compras (fecha, cantidad_entradas, forma_pago_id, usuario_id)
        VALUES (?, ?, ?, ?)
    """, (fecha, cantidad, forma_pago_id, usuario_id))
    compra_id = cur.lastrowid
    con.commit()
    con.close()
    return compra_id

def agregar_entrada_a_compra(compra_id:int, entrada_id:int, precio_aplicado:float):
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = ON;")
    con.execute("""
      INSERT INTO compra_entradas (compra_id, entrada_id, precio_aplicado)
      VALUES (?, ?, ?)
    """, (compra_id, entrada_id, precio_aplicado))
    con.commit()
    con.close()

def get_compra(compra_id:int):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    compra = con.execute("SELECT * FROM compras WHERE id = ?", (compra_id,)).fetchone()
    items = con.execute("""
      SELECT ce.entrada_id, ce.precio_aplicado, e.tipo, e.edad
      FROM compra_entradas ce
      JOIN entradas e ON e.id = ce.entrada_id
      WHERE ce.compra_id = ?
    """, (compra_id,)).fetchall()
    con.close()
    return compra, items

if __name__ == "__main__":
    init_db()
    # Crear una compra (no lunes/feriado, >= hoy). Ej: cambiar fecha según el día actual.
    compra_id = crear_compra(fecha="2025-10-22", cantidad=2, forma_pago_id=2, usuario_id=1)
    agregar_entrada_a_compra(compra_id, 100, 10000.0)
    agregar_entrada_a_compra(compra_id, 101, 7000.0)
    compra, items = get_compra(compra_id)
    print(dict(compra))
    print([dict(i) for i in items])