import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { TiposPaseDb, TipoEntrada } from './tipos-pase-db';

describe('TiposPaseDb', () => {
    let service: TiposPaseDb;
    let httpMock: HttpTestingController;

    beforeEach(() => {
        TestBed.configureTestingModule({
            providers: [
                TiposPaseDb,
                provideHttpClient(),
                provideHttpClientTesting(),
            ],
        });

        service = TestBed.inject(TiposPaseDb);
        httpMock = TestBed.inject(HttpTestingController);
    });

    afterEach(() => {
        httpMock.verify();
    });

    it('getAll > should return all entries', async () => {
        const mock: TipoEntrada[] = [
            { id: 1, nombre: 'VIP' },
            { id: 2, nombre: 'General' },
        ];

        const promise = service.getAll();

        const req = httpMock.expectOne('http://localhost:8000/tipos_entrada');
        expect(req.request.method).toBe('GET');
        req.flush(mock);

        const res = await promise;
        expect(res).toEqual(mock);
    });

});
