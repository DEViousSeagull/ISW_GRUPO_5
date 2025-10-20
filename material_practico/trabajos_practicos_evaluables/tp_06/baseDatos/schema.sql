PRAGMA foreign_keys = ON;

-- 1) Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
  id            INTEGER PRIMARY KEY,
  nombre        TEXT NOT NULL,
  apellido      TEXT NOT NULL,
  email         TEXT NOT NULL UNIQUE
);

-- 2) Formas de pago (catálogo)
CREATE TABLE IF NOT EXISTS formas_pago (
  id      INTEGER PRIMARY KEY,
  nombre  TEXT NOT NULL UNIQUE
  -- opcional: CHECK (nombre IN ('efectivo','tarjeta'))
);

-- 3) Tipos de pase
CREATE TABLE IF NOT EXISTS tipos_pase (
  id     INTEGER PRIMARY KEY,
  nombre TEXT NOT NULL UNIQUE   -- 'VIP', 'General'
);


-- 4) Entradas (item unitario)
-- Guardamos edad, tipo y precio_unitario base; precio_aplicado puede copiarse a la relación con compra.
CREATE TABLE IF NOT EXISTS entradas (
  id               INTEGER PRIMARY KEY,
  edad             INTEGER NOT NULL CHECK (edad >= 0),
  tipo_pase_id     INTEGER NOT NULL REFERENCES tipos_pase(id) ON UPDATE CASCADE ON DELETE RESTRICT,
  precio_unitario  REAL NOT NULL CHECK (precio_unitario >= 0)
);




-- 5) Compras (cabecera)
CREATE TABLE IF NOT EXISTS compras (
  id                     INTEGER PRIMARY KEY,
  fecha                  TEXT NOT NULL,         -- ISO-8601 'YYYY-MM-DD'
  cantidad_entradas      INTEGER NOT NULL CHECK (cantidad_entradas BETWEEN 1 AND 10),
  monto_total            REAL NOT NULL DEFAULT 0,
  forma_pago_id          INTEGER NOT NULL REFERENCES formas_pago(id) ON UPDATE CASCADE ON DELETE RESTRICT,
  usuario_id             INTEGER NOT NULL REFERENCES usuarios(id) ON UPDATE CASCADE ON DELETE RESTRICT,
  mercado_pago_redirect_url TEXT
);

-- 5.a) Restricciones de fecha: no lunes, no pasado, no feriados (01-01 y 12-25)
-- SQLite permite usar strftime en CHECK/trigger; preferimos TRIGGER para mejor control de mensaje.
DROP TRIGGER IF EXISTS trg_compras_fecha_valida;
CREATE TRIGGER trg_compras_fecha_valida
BEFORE INSERT ON compras
FOR EACH ROW
BEGIN
  -- fecha no en el pasado
  SELECT CASE
    WHEN date(NEW.fecha) < date('now', 'localtime')
    THEN RAISE(ABORT, 'La fecha no puede ser anterior a hoy.')
  END;

  -- no lunes (strftime('%w') -> 0=domingo, 1=lunes, ...)
  SELECT CASE
    WHEN strftime('%w', NEW.fecha) = '1'
    THEN RAISE(ABORT, 'La fecha no puede caer en lunes.')
  END;

  -- feriados fijos: 01-01 y 12-25
  SELECT CASE
    WHEN strftime('%m-%d', NEW.fecha) IN ('01-01','12-25')
    THEN RAISE(ABORT, 'La fecha no puede coincidir con un día festivo.')
  END;
END;

-- 6) Relaciones compra <-> entradas (y snapshot de precio)
CREATE TABLE IF NOT EXISTS compra_entradas (
  compra_id        INTEGER NOT NULL REFERENCES compras(id) ON DELETE CASCADE,
  entrada_id       INTEGER NOT NULL REFERENCES entradas(id) ON DELETE RESTRICT,
  precio_aplicado  REAL NOT NULL CHECK (precio_aplicado >= 0),
  PRIMARY KEY (compra_id, entrada_id)
);

-- 6.a) Evitar exceder cantidad_entradas
DROP TRIGGER IF EXISTS trg_no_exceder_cantidad;
CREATE TRIGGER trg_no_exceder_cantidad
BEFORE INSERT ON compra_entradas
FOR EACH ROW
BEGIN
  -- si ya hay N items, no permitir agregar si superaría cantidad_entradas
  SELECT CASE
    WHEN (SELECT COUNT(*) FROM compra_entradas ce WHERE ce.compra_id = NEW.compra_id) >=
         (SELECT cantidad_entradas FROM compras c WHERE c.id = NEW.compra_id)
    THEN RAISE(ABORT, 'No se pueden agregar más entradas que la cantidad declarada en la compra.')
  END;
END;

-- 6.b) Recalcular monto_total después de insertar/eliminar
DROP TRIGGER IF EXISTS trg_recalcular_total_insert;
CREATE TRIGGER trg_recalcular_total_insert
AFTER INSERT ON compra_entradas
FOR EACH ROW
BEGIN
  UPDATE compras
     SET monto_total = (
       SELECT IFNULL(SUM(precio_aplicado), 0)
       FROM compra_entradas
       WHERE compra_id = NEW.compra_id
     )
   WHERE id = NEW.compra_id;
END;

DROP TRIGGER IF EXISTS trg_recalcular_total_delete;
CREATE TRIGGER trg_recalcular_total_delete
AFTER DELETE ON compra_entradas
FOR EACH ROW
BEGIN
  UPDATE compras
     SET monto_total = (
       SELECT IFNULL(SUM(precio_aplicado), 0)
       FROM compra_entradas
       WHERE compra_id = OLD.compra_id
     )
   WHERE id = OLD.compra_id;
END;

