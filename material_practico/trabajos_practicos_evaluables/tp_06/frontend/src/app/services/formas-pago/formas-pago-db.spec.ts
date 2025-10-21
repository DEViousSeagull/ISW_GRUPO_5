import { TestBed } from '@angular/core/testing';

import { FormasPagoDb } from './formas-pago-db';
import { FormaPago } from '../../ts/classes/forma-pago';

describe('FormasPagoDb', () => {
    let service: FormasPagoDb;

    beforeEach(() => {
        TestBed.configureTestingModule({});
        service = TestBed.inject(FormasPagoDb);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    describe('getAll', () => {
        it('should return all entries', async () => {
            const result = await service.getAll();
            expect(result.length).toBeGreaterThan(0);
            expect(result[0]).toBeInstanceOf(FormaPago);
        });
    });

});
