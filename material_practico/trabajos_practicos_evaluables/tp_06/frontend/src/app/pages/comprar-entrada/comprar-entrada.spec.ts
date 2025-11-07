import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule, FormArray, FormGroup } from '@angular/forms';
import { By } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { ComprarEntrada } from './comprar-entrada';
import { routes } from '../../app.routes';
import { provideLocationMocks } from '@angular/common/testing';
import { LOCALE_ID } from '@angular/core';
import { registerLocaleData } from '@angular/common';
import esAR from '@angular/common/locales/es-AR';

import { TiposPaseDb, TipoEntrada } from '../../services/tipos-pase/tipos-pase-db';
import { FormasPagoDb, FormaPago } from '../../services/formas-pago/formas-pago-db';
import { ComprasDb, PostBody, CompraDoc } from '../../services/compras/compras-db';

registerLocaleData(esAR);

describe('ComprarEntrada', () => {
    let component: ComprarEntrada;
    let fixture: ComponentFixture<ComprarEntrada>;
    let form: FormGroup;

    // spies de servicios
    let mockTiposPaseDb: jasmine.SpyObj<TiposPaseDb>;
    let mockFormasPagoDb: jasmine.SpyObj<FormasPagoDb>;
    let mockComprasDb: jasmine.SpyObj<ComprasDb>;

    const TIPOS: TipoEntrada[] = [
        { id: 1, nombre: 'VIP' },
        { id: 2, nombre: 'General' },
    ];
    const FORMAS: FormaPago[] = [
        { id: 1, nombre: 'Efectivo' },
        { id: 2, nombre: 'Tarjeta' },
    ];

    beforeEach(async () => {
        mockTiposPaseDb = jasmine.createSpyObj('TiposPaseDb', ['getAll']);
        mockFormasPagoDb = jasmine.createSpyObj('FormasPagoDb', ['getAll']);
        mockComprasDb = jasmine.createSpyObj('ComprasDb', ['post']);

        mockTiposPaseDb.getAll.and.returnValue(Promise.resolve(TIPOS));
        mockFormasPagoDb.getAll.and.returnValue(Promise.resolve(FORMAS));

        await TestBed.configureTestingModule({
            imports: [ComprarEntrada, ReactiveFormsModule],
            providers: [
                provideRouter(routes),
                provideLocationMocks(),
                { provide: LOCALE_ID, useValue: 'es-AR' },
                { provide: TiposPaseDb, useValue: mockTiposPaseDb },
                { provide: FormasPagoDb, useValue: mockFormasPagoDb },
                { provide: ComprasDb, useValue: mockComprasDb },
            ],
        }).compileComponents();

        fixture = TestBed.createComponent(ComprarEntrada);
        component = fixture.componentInstance;
        await component.ngOnInit(); // carga tipos/forma pago
        fixture.detectChanges();

        form = component.formEntrada;
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    describe('Validaciones del formulario', () => {
        it('debe ser inválido si faltan requeridos', () => {
            form.reset();
            expect(form.valid).toBeFalse();
            expect(form.get('fechaVisita')?.hasError('required')).toBeTrue();
            expect(form.get('cantidadEntradas')?.hasError('required')).toBeTrue();
            expect(form.get('formaPago')?.hasError('required')).toBeTrue();
        });

        it('no debe permitir más de 10 entradas', () => {
            form.patchValue({ cantidadEntradas: 11 });
            component.actualizarVisitantes();
            fixture.detectChanges();

            expect(form.get('cantidadEntradas')?.valid).toBeFalse(); // por max(10)
        });

        it('no debe permitir fecha en el pasado', () => {
            const ayer = new Date();
            ayer.setDate(ayer.getDate() - 1);
            const iso = ayer.toISOString().slice(0, 10);

            form.patchValue({ fechaVisita: iso });
            // dispara validador
            const err = form.get('fechaVisita')?.errors;
            expect(err?.['fechaPasada']).toBeTrue();
        });

        it('la cantidad de visitantes debe coincidir con cantidadEntradas', () => {
            form.patchValue({ cantidadEntradas: 2 });
            component.actualizarVisitantes(); // crea 2 grupos
            fixture.detectChanges();

            // remueve uno para forzar mismatch
            (form.get('visitantes') as FormArray).removeAt(1);
            fixture.detectChanges();

            expect(form.get('visitantes')?.errors?.['visitantesNoCoinciden']).toBeTrue();
            expect(form.valid).toBeFalse();
        });

        it('visitante: edad debe ser entero válido y tipoPase requerido', () => {
            form.patchValue({ cantidadEntradas: 1 });
            component.actualizarVisitantes();
            fixture.detectChanges();

            const vg = (form.get('visitantes') as FormArray).at(0) as FormGroup;
            vg.patchValue({ edad: -2, tipoPase: '' });

            expect(vg.get('edad')?.valid).toBeFalse();
            expect(vg.get('tipoPase')?.valid).toBeFalse();

            vg.patchValue({ edad: 20, tipoPase: 2 });
            expect(vg.valid).toBeTrue();
        });
    });

    describe('Flujo de compra', () => {
        it('muestra el modal de confirmación al postear correctamente y renderiza datos', async () => {
            // fecha siempre futura
            const now = new Date();
            const future = now;
            future.setDate(future.getDate() + 10);
            const isoNow = now.toISOString(); // YYYY-MM-DD
            const isoFuture = future.toISOString().slice(0, 10); // YYYY-MM-DD

            // completar formulario válido
            form.patchValue({
                fechaVisita: isoFuture,
                cantidadEntradas: 2,
                formaPago: 1, // id numérico
            });
            component.actualizarVisitantes();
            fixture.detectChanges();

            const v = (form.get('visitantes') as FormArray);
            v.at(0).patchValue({ edad: 25, tipoPase: 2 }); // General
            v.at(1).patchValue({ edad: 30, tipoPase: 1 }); // VIP

            // asegurarse que el form está válido ANTES de postear
            form.updateValueAndValidity();
            expect(form.valid).toBeTrue();

            // respuesta simulada del backend
            const compraResp: CompraDoc = {
                id: 99,
                fecha: isoFuture,
                fecha_compra: isoNow,
                cantidad_entradas: 2,
                monto_total: 10000,
                forma_pago: { id: 1, nombre: 'Efectivo' },
                usuario: { id: 1, nombre: 'Juan', apellido: 'Pérez', email: 'juan@example.com' },
                entradas: [
                    { id: 1, precio_unitario: 5000, edad: 25, tipo_entrada: { id: 2, nombre: 'General' } },
                    { id: 2, precio_unitario: 5000, edad: 30, tipo_entrada: { id: 1, nombre: 'VIP' } },
                ],
            };
            mockComprasDb.post.and.returnValue(
                Promise.resolve({ mensaje: 'creada', compra: compraResp })
            );

            await component.submitForm();
            fixture.detectChanges();

            expect(mockComprasDb.post).toHaveBeenCalled();
            expect(component.confirmModalVisible).toBeTrue();
            expect(component.detalleCompra?.id).toBe(99);

            const modal = fixture.debugElement.query(By.css('.modal-card'));
            expect(modal).toBeTruthy();

            const modalText = modal.nativeElement.textContent.replace(/\s+/g, ' ');
            // La fecha renderizada con el DatePipe debe coincidir con iso en formato dd/MM/yyyy
            const [y, m, d] = isoFuture.split('-');
            const ddmmyyyy = `${d}/${m}/${y}`;
            expect(modalText).toContain('Compra confirmada');
            expect(modalText).toContain(ddmmyyyy);
            expect(modalText).toMatch(/10\.000/);
            expect(modalText).toContain('juan@example.com');
        });


        it('si el formulario es inválido, no postea y enfoca el primer error', async () => {
            form.reset();
            await component.submitForm();
            expect(mockComprasDb.post).not.toHaveBeenCalled();
            // no podemos verificar scrollIntoView, pero el modal no debe estar visible
            expect(component.confirmModalVisible).toBeFalse();
        });
    });
});
