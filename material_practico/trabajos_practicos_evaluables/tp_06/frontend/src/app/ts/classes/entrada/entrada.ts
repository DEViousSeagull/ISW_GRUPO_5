import { TipoPase } from "./tipo-pase";

export class Entrada {
    constructor(
        public id: string,
        public tipo: TipoPase,
        public edad: number,
        public precio: number
    ) {
    }
}