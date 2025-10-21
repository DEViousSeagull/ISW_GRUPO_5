import { TestBed } from '@angular/core/testing';
import { TiposPaseDb } from './tipos-pase-db';
import { TipoPase } from '../../ts/classes/entrada/tipo-pase';

describe('TiposPaseDb', () => {
    let service: TiposPaseDb;

    beforeEach(() => {
        TestBed.configureTestingModule({});
        service = TestBed.inject(TiposPaseDb);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    describe('getAll', () => {
        it('should return all entries', async () => {
            const result = await service.getAll();
            expect(result.length).toBeGreaterThan(0);
            expect(result[0]).toBeInstanceOf(TipoPase);
        });
    });
});
