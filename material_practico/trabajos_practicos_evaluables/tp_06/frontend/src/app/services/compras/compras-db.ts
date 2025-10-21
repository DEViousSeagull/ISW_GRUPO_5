import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';


// entrada.model.ts
export interface TipoEntrada {
    nombre: string;
}

export interface Entrada {
    id: number;
    precio: number;
    edad: number;
    tipo_entrada: TipoEntrada;
}

export interface FormaPago {
    id: number;
    nombre: string;
}

export interface Usuario {
    id: number;
    nombre: string;
    apellido: string;
    email: string;
}

export interface Compra {
    id: number;
    fecha: string; // ISO date from backend
    cantidad_entradas: number;
    monto_total: number;
    forma_pago: FormaPago;
    usuario: Usuario;
    entradas: Entrada[];
}

export const MOCK_COMPRAS: Compra[] = [
    {
        id: 1,
        fecha: '2025-10-21',
        cantidad_entradas: 1,
        monto_total: 5000,
        forma_pago: { id: 1, nombre: 'Efectivo' },
        usuario: { id: 1, nombre: 'Juan', apellido: 'Pérez', email: 'juan@example.com' },
        entradas: [
            {
                id: 1,
                precio: 5000,
                edad: 30,
                tipo_entrada: { nombre: 'General' }
            }
        ]
    },
];

@Injectable({
    providedIn: 'root'
})
export class ComprasDb {

    private readonly baseUrl = 'http://localhost:8000/compras'; // adjust if needed
    private useMock = true; // toggle between mock and real API

    constructor(private http: HttpClient) { }

    async getAll(): Promise<Compra[]> {
        if (this.useMock) {
            // simulate async delay
            return new Promise(resolve => setTimeout(() => resolve(MOCK_COMPRAS), 300));
        }

        return firstValueFrom(this.http.get<Compra[]>(this.baseUrl));
    }

    async getById(id: number): Promise<Compra | undefined> {
        if (this.useMock) {
            // reuse mock data
            const all = await this.getAll();
            return all.find(c => c.id === id);
        }

        return firstValueFrom(this.http.get<Compra>(`${this.baseUrl}/${id}`));
    }
}
