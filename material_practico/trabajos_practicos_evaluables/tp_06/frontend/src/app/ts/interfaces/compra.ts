export interface CompraDoc {
    id: string,
    fecha: string,
    cantidadEntradas: number,
    idsEntrada: Array<string>,
    montoTotal: number
}