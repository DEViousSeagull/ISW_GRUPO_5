import { ComponentFixture, TestBed } from '@angular/core/testing';
import { DetalleCompra } from './detalle-compra';
import { CompraDoc, ComprasDb } from '../../services/compras/compras-db';
import { ActivatedRoute } from '@angular/router';
import { By } from '@angular/platform-browser';
import { LOCALE_ID } from '@angular/core';
import { registerLocaleData } from '@angular/common';
import esAR from '@angular/common/locales/es-AR';

registerLocaleData(esAR);

describe('DetalleCompra', () => {
    let component: DetalleCompra;
    let fixture: ComponentFixture<DetalleCompra>;
    let mockDb: jasmine.SpyObj<ComprasDb>;

    const fakeCompra: CompraDoc = {
        id: 1,
        fecha: '2025-10-22',
        fecha_compra: '2025-10-21T21:24:34-03:00',
        cantidad_entradas: 2,
        monto_total: 10000,
        forma_pago: { id: 1, nombre: 'Efectivo' },
        usuario: { id: 1, nombre: 'Juan', apellido: 'Pérez', email: 'juan@example.com' },
        entradas: [
            { id: 1, precio_unitario: 5000, edad: 25, tipo_entrada: { id: 2, nombre: 'General' } },
            { id: 2, precio_unitario: 5000, edad: 30, tipo_entrada: { id: 1, nombre: 'VIP' } }
        ]
    };

    beforeEach(async () => {
        mockDb = jasmine.createSpyObj('ComprasDb', ['getById']);

        await TestBed.configureTestingModule({
            imports: [DetalleCompra], // es standalone: alcanza con importar el componente
            providers: [
                { provide: ComprasDb, useValue: mockDb },
                { provide: LOCALE_ID, useValue: 'es-AR' },
                {
                    provide: ActivatedRoute,
                    useValue: { snapshot: { paramMap: { get: () => '1' } } }
                }
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(DetalleCompra);
        component = fixture.componentInstance;
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should load compra and entries on init', async () => {
        mockDb.getById.and.returnValue(Promise.resolve(fakeCompra));

        await component.ngOnInit();
        fixture.detectChanges();

        expect(component.compra).toEqual(fakeCompra);
        expect(component.entradas.length).toBe(2);

        // Info de compra en el DOM
        const compraInfo = fixture.debugElement.query(By.css('.compra-info'));
        const text = compraInfo.nativeElement.textContent;

        // Fecha con DatePipe y locale es-AR
        expect(text).toContain('21/10/2025');

        // Cantidad
        expect(text).toContain('Cantidad de entradas:');
        expect(text).toContain('2');

        // Monto total con CurrencyPipe y formato '1.0-0' -> $ 10.000 (sin decimales)
        // según fuente puede renderear como "$ 10.000" o "ARS 10.000"; validamos el número:
        expect(text.replace(/\s+/g, ' ')).toMatch(/10\.000/);

        // Tabla de entradas (3 columnas: Tipo, Edad, Precio)
        const rows = fixture.debugElement.queryAll(By.css('.tabla-compras tbody tr'));
        expect(rows.length).toBe(2);

        const firstRowCells = rows[0].queryAll(By.css('td'));
        expect(firstRowCells[0].nativeElement.textContent).toContain('General');
        expect(firstRowCells[1].nativeElement.textContent).toContain('25');
        expect(firstRowCells[2].nativeElement.textContent.replace(/\s+/g, ' ')).toMatch(/5\.000/);

        const secondRowCells = rows[1].queryAll(By.css('td'));
        expect(secondRowCells[0].nativeElement.textContent).toContain('VIP');
    });

    it('should show error if compra not found', async () => {
        mockDb.getById.and.returnValue(Promise.resolve(undefined));

        await component.ngOnInit();
        fixture.detectChanges();

        expect(component.error).toContain('No se encontró la compra');
        const errorElem = fixture.debugElement.query(By.css('.error, .empty'));
        expect(errorElem.nativeElement.textContent).toContain('No se encontró la compra');
    });

    it('should handle invalid ID param', async () => {
        const route = TestBed.inject(ActivatedRoute);
        spyOn(route.snapshot.paramMap, 'get').and.returnValue(null);

        await component.ngOnInit();
        fixture.detectChanges();

        expect(component.error).toContain('No se especificó la compra');
    });
});
