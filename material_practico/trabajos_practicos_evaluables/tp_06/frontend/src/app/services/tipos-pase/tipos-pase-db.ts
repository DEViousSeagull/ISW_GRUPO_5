import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';

export interface TipoEntrada {
    id: number;
    nombre: string;
}

@Injectable({
    providedIn: 'root'
})
export class TiposPaseDb {
    private baseUrl = 'http://localhost:8000/tipos_entrada';

    constructor(private httpClient: HttpClient) { }

    getAll(): Promise<TipoEntrada[]> {
        return firstValueFrom(this.httpClient.get<TipoEntrada[]>(this.baseUrl));
    }
}
