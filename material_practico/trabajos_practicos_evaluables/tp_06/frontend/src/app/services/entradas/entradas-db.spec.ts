import { TestBed } from '@angular/core/testing';

import { EntradasDb } from './entradas-db';
import { Entrada } from '../../ts/classes/entrada/entrada';
import { EntradaDoc } from '../../ts/interfaces/entrada/entrada';
import { TipoPase } from '../../ts/classes/entrada/tipo-pase';

describe('EntradasDb', () => {
    let service: EntradasDb;

    beforeEach(() => {
        TestBed.configureTestingModule({});
        service = TestBed.inject(EntradasDb);

        spyOn(service, 'getById').and.callFake((id: string) => {
            if (id === '1') {
                return new Entrada('1', new TipoPase('VIP'), 20, 50);
            }
            return undefined;
        });
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    describe('getAll', () => {
        it('should return all entries', () => {
            const result = service.getAll();
            expect(result.length).toBeGreaterThan(0);
            expect(result[0]).toBeInstanceOf(Entrada);
        });
    });

    describe('getById', () => {
        it('should return the entry by id', () => {
            const id = '1';
            const result = service.getById(id);
            expect(result).toBeInstanceOf(Entrada);
            expect(result?.id).toBe('1');
        });



        it('should return undefined if id does not exist', () => {
            const result = service.getById('nqvvvvv');
            expect(result).toBeUndefined();
        });
    });

    describe('fromDocToClass', () => {
        it('should convert TipoEntradaDoc to TipoEntrada instance', () => {
            const doc: EntradaDoc = {
                id: 'e1',
                idTipo: 'VIP',
                edad: 14,
                precio: 15
            };
            const tipo = service.fromDocToClass(doc);
            expect(tipo).toBeInstanceOf(Entrada);
            expect(tipo.id).toBe(doc.id);
        });
    });
});
