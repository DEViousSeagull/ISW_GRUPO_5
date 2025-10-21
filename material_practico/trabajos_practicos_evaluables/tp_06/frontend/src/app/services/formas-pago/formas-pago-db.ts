import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { FormaPago } from '../../ts/classes/forma-pago';
import { firstValueFrom } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class FormasPagoDb {
    private baseUrl = 'http://localhost:8000/formas_pago';

    constructor(private httpClient: HttpClient) { }

    getAll(): Promise<FormaPago[]> {
        return firstValueFrom(this.httpClient.get<FormaPago[]>(this.baseUrl));
    }
}
