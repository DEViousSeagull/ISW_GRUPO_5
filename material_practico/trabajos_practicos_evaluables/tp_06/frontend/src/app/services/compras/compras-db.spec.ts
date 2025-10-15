import { EntradasDb } from './../entradas/entradas-db';
import { TestBed } from '@angular/core/testing';
import { ComprasDb } from './compras-db';
import { TipoPase } from '../../ts/classes/entrada/tipo-pase';
import { Entrada } from '../../ts/classes/entrada/entrada';
import { EntradaDoc } from '../../ts/interfaces/entrada/entrada';
import { CompraDoc } from '../../ts/interfaces/compra';
import { Compra } from '../../ts/classes/compra';


describe('ComprasDb', () => {
    let service: ComprasDb;
    let entradasDbMock: Partial<EntradasDb>;

    beforeEach(() => {
        entradasDbMock = {
            getById: (id: string) => ({ id, tipo: new TipoPase('VIP'), edad: 20, precio: 100 }),
            fromDocToClass: (doc: EntradaDoc) => new Entrada(doc.id, new TipoPase(doc.idTipo), doc.edad, doc.precio)
        };

        TestBed.configureTestingModule({});
        service = new ComprasDb(entradasDbMock as EntradasDb);
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    describe('getAll', () => {
        it('should return all compras', async () => {
            const doc: CompraDoc = { id: '1', fecha: new Date().toISOString(), cantidadEntradas: 1, idsEntrada: ['e1'], montoTotal: 100 };
            await service.create(doc);
            const all = await service.getAll();
            expect(all.length).toBe(1);
            expect(all[0].id).toBe('1');
        });
    });

    describe('getById', () => {
        it('should return compra by id', async () => {
            const doc: CompraDoc = { id: '2', fecha: new Date().toISOString(), cantidadEntradas: 1, idsEntrada: ['e1'], montoTotal: 100 };
            await service.create(doc);
            const compra = await service.getById('2');
            expect(compra).toBeDefined();
            expect(compra?.montoTotal).toBe(100);
        });

        it('should return undefined for non-existent id', async () => {
            const compra = await service.getById('999999999999999999');
            expect(compra).toBeUndefined();
        });
    });

    describe('create', () => {
        it('should add a new compra', async () => {
            const doc: CompraDoc = { id: '3', fecha: new Date().toISOString(), cantidadEntradas: 1, idsEntrada: ['e1'], montoTotal: 100 };
            await service.create(doc);
            const docs = await service.getAll();
            expect(docs).toContain(doc);
        });
    });

    describe('fromDocToClass', () => {
        it('should convert CompraDoc to Compra instance', () => {
            const doc = { id: '4', fecha: new Date().toISOString(), cantidadEntradas: 1, idsEntrada: ['e1'], montoTotal: 100 };
            const compra = service.fromDocToClass(doc);
            expect(compra).toBeInstanceOf(Compra);
            expect(compra.entradas[0]).toBeInstanceOf(Entrada);
            expect(compra.montoTotal).toBe(100);
        });

        it('should throw if an entrada id is not found', () => {
            const doc = { id: '5', fecha: new Date().toISOString(), cantidadEntradas: 1, idsEntrada: ['missing'], montoTotal: 100 };
            entradasDbMock.getById = () => undefined;
            service = new ComprasDb(entradasDbMock as EntradasDb);
            expect(() => service.fromDocToClass(doc)).toThrowError(/Entrada con id/);
        });
    });

    describe('fromClassToDoc', () => {
        it('should convert Compra instance to CompraDoc', () => {
            const entrada = new Entrada('e1', new TipoPase('VIP'), 25, 150);
            const compra = new Compra('6', new Date('2025-10-15'), 1, [entrada], 150);
            const doc = service.fromClassToDoc(compra);
            expect(doc.id).toBe('6');
            expect(doc.idsEntrada).toEqual(['e1']);
            expect(doc.montoTotal).toBe(150);
        });
    });
});
