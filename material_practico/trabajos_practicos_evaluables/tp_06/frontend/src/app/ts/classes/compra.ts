import { Entrada } from "./entrada/entrada";

export class Compra {
    constructor(
        public id: string,
        public fecha: Date,
        public cantidadEntradas: number,
        public entradas: Array<Entrada>,
        public montoTotal: number
    ) {

        if (entradas.length !== cantidadEntradas) throw "Entradas no coincide con cantidadEntradas";
        
        const total = entradas.reduce((acc, e) => e.precio + acc, 0);
        if(total !== montoTotal) throw "Total de entradas no coincide con montoTotal";
    }
}