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
        it('should return all entries', () => {
            const result = service.getAll();
            expect(result.length).toBeGreaterThan(0);
            expect(result[0]).toBeInstanceOf(TipoPase);
        });
    });

    describe('getById', () => {
        it('should return the entry (VIP) by id', () => {
            const id = 'VIP';
            const result = service.getById(id);
            expect(result).toBeInstanceOf(TipoPase);
            expect(result?.nombre).toBe('VIP');
        });

        it('should return the entry (regular) by id', () => {
            const id = 'regular';
            const result = service.getById(id);
            expect(result).toBeInstanceOf(TipoPase);
            expect(result?.nombre).toBe('regular');
        });

        it('should return undefined if id does not exist', () => {
            const result = service.getById('nqvvvvv');
            expect(result).toBeUndefined();
        });
    });

    describe('fromDocToClass', () => {
        it('should convert TipoEntradaDoc to TipoEntrada instance', () => {
            const doc = { nombre: 'VIP' };
            const tipo = service.fromDocToClass(doc);
            expect(tipo).toBeInstanceOf(TipoPase);
            expect(tipo.nombre).toBe(doc.nombre);
        });
    });
});
