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
        it('should return all entries', () => {
            const result = service.getAll();
            expect(result.length).toBeGreaterThan(0);
            expect(result[0]).toBeInstanceOf(FormaPago);
        });
    });

    describe('getById', () => {
        it('should return the entry (efectivo) by id', () => {
            const id = 'efectivo';
            const result = service.getById(id);
            expect(result).toBeInstanceOf(FormaPago);
            expect(result?.nombre).toBe('efectivo');
        });

        it('should return the entry (tarjeta) by id', () => {
            const id = 'tarjeta';
            const result = service.getById(id);
            expect(result).toBeInstanceOf(FormaPago);
            expect(result?.nombre).toBe('tarjeta');
        });

        it('should return undefined if id does not exist', () => {
            const result = service.getById('nqvvvvv');
            expect(result).toBeUndefined();
        });
    });

    describe('fromDocToClass', () => {
        it('should convert TipoEntradaDoc to TipoEntrada instance', () => {
            const doc = { nombre: 'efectivo' };
            const tipo = service.fromDocToClass(doc);
            expect(tipo).toBeInstanceOf(FormaPago);
            expect(tipo.nombre).toBe(doc.nombre);
        });
    });
});
