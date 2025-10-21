import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface TipoEntrada {
    id: number;
    nombre: string;
}

@Injectable({
    providedIn: 'root'
})
export class TiposPaseDb {
    private baseUrl = 'http://localhost:8000/tipos-entrada';

    constructor(private httpClient: HttpClient) { }

    getAll(): Observable<TipoEntrada[]> {
        return this.httpClient.get<TipoEntrada[]>(this.baseUrl);
    }
}
