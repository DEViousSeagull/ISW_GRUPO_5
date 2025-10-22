import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MisCompras } from './mis-compras';
import { ComprasDb, CompraDoc } from '../../services/compras/compras-db';
import { Router } from '@angular/router';
import { By } from '@angular/platform-browser';
import { LOCALE_ID } from '@angular/core';
import { registerLocaleData } from '@angular/common';
import esAR from '@angular/common/locales/es-AR';

registerLocaleData(esAR);

describe('MisCompras', () => {
    let component: MisCompras;
    let fixture: ComponentFixture<MisCompras>;
    let mockDb: jasmine.SpyObj<ComprasDb>;
    let mockRouter: jasmine.SpyObj<Router>;

    const fakeCompras: CompraDoc[] = [
        {
            id: 1,
            fecha: '2025-10-22',
            fecha_compra: '2025-10-21T21:24:34-03:00', // 21/10/2025
            cantidad_entradas: 2,
            monto_total: 10000,
            forma_pago: { id: 1, nombre: 'Efectivo' },
            usuario: { id: 1, nombre: 'Juan', apellido: 'Pérez', email: 'juan@example.com' },
            entradas: []
        },
        {
            id: 2,
            fecha: '2025-11-01',
            fecha_compra: '2025-11-01T10:15:00-03:00', // 01/11/2025
            cantidad_entradas: 1,
            monto_total: 5000,
            forma_pago: { id: 2, nombre: 'Tarjeta' },
            usuario: { id: 2, nombre: 'Ana', apellido: 'Gómez', email: 'ana@example.com' },
            entradas: []
        }
    ];

    beforeEach(async () => {
        mockDb = jasmine.createSpyObj('ComprasDb', ['getAll']);
        mockRouter = jasmine.createSpyObj('Router', ['navigate']);

        await TestBed.configureTestingModule({
            imports: [MisCompras], // standalone component
            providers: [
                { provide: ComprasDb, useValue: mockDb },
                { provide: Router, useValue: mockRouter },
                { provide: LOCALE_ID, useValue: 'es-AR' },
            ]
        }).compileComponents();

        fixture = TestBed.createComponent(MisCompras);
        component = fixture.componentInstance;
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should load compras on init', async () => {
        mockDb.getAll.and.returnValue(Promise.resolve(fakeCompras));

        await component.ngOnInit();
        fixture.detectChanges();

        expect(component.compras.length).toBe(2);

        const cards = fixture.debugElement.queryAll(By.css('.compra-card'));
        expect(cards.length).toBe(2);

        const text1 = cards[0].nativeElement.textContent.replace(/\s+/g, ' ');
        const text2 = cards[1].nativeElement.textContent.replace(/\s+/g, ' ');

        // Fechas en es-AR
        expect(text1).toContain('21/10/2025');
        expect(text2).toContain('01/11/2025');

        // Monto: permitir variaciones de símbolo/espacios, pero validar el número formateado
        expect(text1).toMatch(/10\.000/);
        expect(text2).toMatch(/5\.000/);
    });

    it('should show loading initially', () => {
        component.loading = true;
        fixture.detectChanges();

        const loadingElem = fixture.debugElement.query(By.css('.loading'));
        expect(loadingElem).toBeTruthy();
        expect(loadingElem.nativeElement.textContent).toContain('Cargando compras');
    });

    it('should show error message', () => {
        component.error = 'Error al cargar';
        component.loading = false;
        fixture.detectChanges();

        const errorElem = fixture.debugElement.query(By.css('.error'));
        expect(errorElem).toBeTruthy();
        expect(errorElem.nativeElement.textContent).toContain('Error al cargar');
    });

    it('should show empty message when no compras', () => {
        component.compras = [];
        component.loading = false;
        fixture.detectChanges();

        const emptyElem = fixture.debugElement.query(By.css('.empty'));
        expect(emptyElem).toBeTruthy();
        // En el template termina con punto; usamos "toContain" para ser tolerantes
        expect(emptyElem.nativeElement.textContent).toContain('No tenés compras registradas');
    });

    it('should navigate to mis-compras on card click', async () => {
        mockDb.getAll.and.returnValue(Promise.resolve(fakeCompras));

        await component.ngOnInit();
        fixture.detectChanges();

        const firstCard = fixture.debugElement.queryAll(By.css('.compra-card'))[0];
        firstCard.triggerEventHandler('click', null);

        expect(mockRouter.navigate).toHaveBeenCalledWith(['/mis-compras', 1]);
    });
});
