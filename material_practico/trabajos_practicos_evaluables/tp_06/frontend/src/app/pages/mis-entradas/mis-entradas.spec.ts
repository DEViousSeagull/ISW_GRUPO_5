import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MisEntradas } from './mis-entradas';
import { ComprasDb, Compra, Entrada } from '../../services/compras/compras-db';
import { ActivatedRoute } from '@angular/router';
import { of } from 'rxjs';
import { CommonModule, DatePipe, CurrencyPipe } from '@angular/common';
import { By } from '@angular/platform-browser';

describe('MisEntradas', () => {
    let component: MisEntradas;
    let fixture: ComponentFixture<MisEntradas>;
    let mockDb: jasmine.SpyObj<ComprasDb>;
    const fakeCompra: Compra = {
        id: 1,
        fecha: '2025-10-21',
        cantidad_entradas: 2,
        monto_total: 10000,
        forma_pago: { id: 1, nombre: 'Efectivo' },
        usuario: { id: 1, nombre: 'Juan', apellido: 'Pérez', email: 'juan@example.com' },
        entradas: [
            { id: 1, precio: 5000, edad: 25, tipo_entrada: { nombre: 'General' } },
            { id: 2, precio: 5000, edad: 30, tipo_entrada: { nombre: 'VIP' } }
        ]
    };

    beforeEach(async () => {
        mockDb = jasmine.createSpyObj('ComprasDb', ['getById']);

        await TestBed.configureTestingModule({
            imports: [MisEntradas, CommonModule, DatePipe, CurrencyPipe],
            providers: [
                { provide: ComprasDb, useValue: mockDb },
                {
                    provide: ActivatedRoute,
                    useValue: { snapshot: { paramMap: { get: () => '1' } } }
                }
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(MisEntradas);
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

        // Check compra info in DOM
        const compraInfo = fixture.debugElement.query(By.css('.compra-info'));
        expect(compraInfo.nativeElement.textContent).toContain('21/10/2025');
        expect(compraInfo.nativeElement.textContent).toContain('2');
        expect(compraInfo.nativeElement.textContent).toContain('10.000');

        // Check entries table
        const tableRows = fixture.debugElement.queryAll(By.css('.tabla-compras tbody tr'));
        expect(tableRows.length).toBe(2);

        const firstRowCells = tableRows[0].queryAll(By.css('td'));
        expect(firstRowCells[0].nativeElement.textContent).toContain('1');
        expect(firstRowCells[1].nativeElement.textContent).toContain('General');
        expect(firstRowCells[2].nativeElement.textContent).toContain('25');
        expect(firstRowCells[3].nativeElement.textContent).toContain('5.000');

        const secondRowCells = tableRows[1].queryAll(By.css('td'));
        expect(secondRowCells[1].nativeElement.textContent).toContain('VIP');
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
