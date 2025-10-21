import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';


// entrada.model.ts
export interface TipoEntradaDoc {
    id: number;
    nombre: string;
}

export interface EntradaDoc {
    id: number;
    precio_unitario: number;
    edad: number;
    tipo_entrada: TipoEntradaDoc;
}

export interface FormaPagoDoc {
    id: number;
    nombre: string;
}

export interface UsuarioDoc {
    id: number;
    nombre: string;
    apellido: string;
    email: string;
}

export interface CompraDoc {
    id: number;
    fecha: string; // ISO date from backend
    cantidad_entradas: number;
    monto_total: number;
    forma_pago: FormaPagoDoc;
    usuario: UsuarioDoc;
    entradas: EntradaDoc[];
}

export const MOCK_COMPRAS: CompraDoc[] = [
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
                precio_unitario: 5000,
                edad: 30,
                tipo_entrada: { id: 2, nombre: 'General' }
            }
        ]
    },
];

export interface PostBody {
    fecha: string, // "2025-10-21",
    cantidad_entradas: number,
    usuario: {
        id: number
    },
    forma_pago: {
        id: number
    },
    entradas: Array<{
        edad: number,
        tipo_entrada: { id: number }
    }>
}

interface PostResponse {
    mensaje: string,
    compra: CompraDoc
}

@Injectable({
    providedIn: 'root'
})
export class ComprasDb {

    private readonly baseUrl = 'http://localhost:8000/compras'; // adjust if needed
    private useMock = true; // toggle between mock and real API

    constructor(private http: HttpClient) { }

    async getAll(): Promise<CompraDoc[]> {
        // if (this.useMock) {
        //     // simulate async delay
        //     return new Promise(resolve => setTimeout(() => resolve(MOCK_COMPRAS), 300));
        // }

        return firstValueFrom(this.http.get<Array<CompraDoc>>(this.baseUrl));
    }

    async getById(id: number): Promise<CompraDoc | undefined> {
        if (true) {
            // reuse mock data
            const all = await this.getAll();
            return all.find(c => c.id === id);
        }

        // return firstValueFrom(this.http.get<Compra>(`${this.baseUrl}/${id}`));
    }

    async post(post: PostBody): Promise<PostResponse> {
        return firstValueFrom(this.http.post<PostResponse>(`${this.baseUrl}/crear_compra`, post));
    }

}
