import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { CompraDoc, ComprasDb, PostBody } from './compras-db';

describe('ComprasDb', () => {
    let service: ComprasDb;
    let httpMock: HttpTestingController;

    const SAMPLE_COMPRA: CompraDoc = {
        id: 1,
        fecha: '2025-10-21',
        cantidad_entradas: 1,
        monto_total: 5000,
        forma_pago: { id: 1, nombre: 'Efectivo' },
        usuario: { id: 1, nombre: 'Juan', apellido: 'Pérez', email: 'juan@example.com' },
        entradas: [
            {
                id: 1,
                precio_unitario: 5000,
                edad: 30,
                tipo_entrada: { id: 2, nombre: 'General' }
            }
        ]
    };

    beforeEach(() => {
        TestBed.configureTestingModule({
            imports: [HttpClientTestingModule],
            providers: [ComprasDb],
        });

        service = TestBed.inject(ComprasDb);
        httpMock = TestBed.inject(HttpTestingController);
    });

    afterEach(() => {
        httpMock.verify(); // no queden requests pendientes
    });

    it('should be created', () => {
        expect(service).toBeTruthy();
    });

    describe('getAll', () => {
        it('should return all compras (filtradas por MOCK_USER.id)', async () => {
            const promise = service.getAll();

            const req = httpMock.expectOne('http://localhost:8000/compras');
            expect(req.request.method).toBe('GET');

            // devolvemos la compra que “siempre existe”
            req.flush([SAMPLE_COMPRA]);

            const all = await promise;
            expect(all.length).toBe(1);
            expect(all[0].id).toBe(1);
        });
    });

    describe('getById', () => {
        it('should return compra by id', async () => {
            const promise = service.getById(1);

            // getById internamente llama a getAll() -> 1 GET a /compras
            const req = httpMock.expectOne('http://localhost:8000/compras');
            expect(req.request.method).toBe('GET');
            req.flush([SAMPLE_COMPRA]);

            const compra = await promise;
            expect(compra).toBeDefined();
            expect(compra?.id).toBe(1);
            expect(compra?.monto_total).toBe(5000);
        });

        it('should return undefined for non-existent id', async () => {
            const promise = service.getById(999999);

            const req = httpMock.expectOne('http://localhost:8000/compras');
            expect(req.request.method).toBe('GET');
            req.flush([SAMPLE_COMPRA]);

            const compra = await promise;
            expect(compra).toBeUndefined();
        });
    });

    describe('post', () => {
        it('should add a new compra (POST /compras/crear_compra)', async () => {
            const body: PostBody = {
                fecha: '2027-10-21',
                cantidad_entradas: 2,
                usuario: { id: 1 },
                forma_pago: { id: 1 },
                entradas: [
                    { edad: 30, tipo_entrada: { id: 2 } }
                ]
            };

            const serverResponse = {
                mensaje: 'creada',
                compra: {
                    ...SAMPLE_COMPRA,
                    id: 2,
                    fecha: '2027-10-21',
                    cantidad_entradas: 2,
                    monto_total: 10000
                }
            };

            const promise = service.post(body);

            const req = httpMock.expectOne('http://localhost:8000/compras/crear_compra');
            expect(req.request.method).toBe('POST');
            expect(req.request.body).toEqual(body);

            req.flush(serverResponse);

            const res = await promise;
            expect(res.mensaje).toBe('creada');
            expect(res.compra.id).toBe(2);
            expect(res.compra.cantidad_entradas).toBe(2);
        });
    });
});
