import { TestBed } from '@angular/core/testing';

import { FormasPagoDb } from './formas-pago-db';
import { FormaPagoDoc } from '../compras/compras-db';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { provideHttpClient } from '@angular/common/http';

describe('FormasPagoDb', () => {
    let service: FormasPagoDb;
    let httpMock: HttpTestingController;

    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                FormasPagoDb,
                provideHttpClient(),
                provideHttpClientTesting(),
            ],
        });

        service = TestBed.inject(FormasPagoDb);
        httpMock = TestBed.inject(HttpTestingController);
    });

    afterEach(() => {
        httpMock.verify();
    });

    it('getAll > should return all entries', async () => {
        const mock: FormaPagoDoc[] = [
            { id: 1, nombre: 'Efectivo' },
            { id: 2, nombre: 'Tarjeta' },
        ];

        const promise = service.getAll();

        const req = httpMock.expectOne('http://localhost:8000/formas_pago');
        expect(req.request.method).toBe('GET');
        req.flush(mock);

        const res = await promise;
        expect(res).toEqual(mock);
    });


});
