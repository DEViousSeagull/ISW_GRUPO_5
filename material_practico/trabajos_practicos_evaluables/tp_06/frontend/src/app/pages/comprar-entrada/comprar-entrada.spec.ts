import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule, FormGroup, FormsModule } from '@angular/forms';
import { By } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { ComprarEntrada } from './comprar-entrada';
import { routes } from '../../app.routes';
import { provideLocationMocks } from '@angular/common/testing';

describe('ComprarEntrada', () => {
    let component: ComprarEntrada;
    let formEntrada: FormGroup;
    let fixture: ComponentFixture<ComprarEntrada>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [ComprarEntrada, ReactiveFormsModule, FormsModule],
            providers: [provideRouter(routes), provideLocationMocks()]
        }).compileComponents();

        fixture = TestBed.createComponent(ComprarEntrada);
        component = fixture.componentInstance;
        formEntrada = component.buildForm();
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    describe('Formulario de compra', () => {
        it('debe ser inválido si no se completan los campos requeridos', () => {
            formEntrada.patchValue({
                fechaVisita: '',
                cantidadEntradas: null,
                edades: [],
                tipoPase: '',
                formaPago: ''
            });
            expect(formEntrada.valid).toBeFalse();
        });

        it('no debe permitir más de 10 entradas', () => {
            formEntrada.patchValue({
                fechaVisita: new Date(),
                cantidadEntradas: 11,
                edades: [30, 25, 20, 30, 25, 20, 30, 25, 20, 23, 11],
                tipoPase: 'regular',
                formaPago: 'efectivo'
            });
            expect(formEntrada.valid).toBeFalse();
        });

        it('no debe permitir fecha en la cual el parque está cerrado', () => {
            const fechaCerrado = new Date('2025-10-19'); // ejemplo de día cerrado
            formEntrada.patchValue({
                fechaVisita: fechaCerrado,
                cantidadEntradas: 2,
                edades: [25, 30],
                tipoPase: 'VIP',
                formaPago: 'efectivo'
            });

            expect(formEntrada.valid).toBeFalse();
        });

        it('no debe permitir una fecha de visita pasada', () => {
            // Fecha pasada (ayer)
            const fechaPasada = new Date();
            fechaPasada.setDate(fechaPasada.getDate() - 1);

            formEntrada.patchValue({
                fechaVisita: fechaPasada,
                cantidadEntradas: 2,
                edades: [25, 30],
                tipoPase: 'VIP',
                formaPago: 'efectivo'
            });
            expect(formEntrada.valid).toBeFalse();
        });


        it('la cantidad de edades debe coincidir con la cantidad de entradas', () => {
            formEntrada.patchValue({
                fechaVisita: new Date(),
                cantidadEntradas: 3,
                edades: [25, 30], // solo 2 edades -> inválido
                tipoPase: 'VIP',
                formaPago: 'efectivo'
            });

            expect(formEntrada.valid).toBeFalse();
        });

        it('la cantidad de entradas debe ser un número entero positivo', () => {
            formEntrada.patchValue({
                fechaVisita: new Date(),
                cantidadEntradas: -2,
                edades: [],
                tipoPase: 'regular',
                formaPago: 'efectivo'
            });
            expect(formEntrada.valid).toBeFalse();

            formEntrada.patchValue({ cantidadEntradas: 2.5 });
            expect(formEntrada.valid).toBeFalse();
        });

        it('las edades deben ser un número entero positivo', () => {
            formEntrada.patchValue({
                fechaVisita: new Date(),
                cantidadEntradas: 1,
                edades: [-2],
                tipoPase: 'regular',
                formaPago: 'efectivo'
            });
            expect(formEntrada.valid).toBeFalse();

            formEntrada.patchValue({ cantidadEntradas: 2.5 });
            expect(formEntrada.valid).toBeFalse();
        });
    });

    describe('Flujo de compra', () => {


        it('debe informar cantidad de entradas y fecha al finalizar', () => {

            spyOn(component, 'mostrarResumenCompra');

            formEntrada.patchValue({
                fechaVisita: new Date('2025-10-15'),
                cantidadEntradas: 3,
                edades: [20, 25, 30],
                tipoPase: 'regular',
                formaPago: 'efectivo'
            });

            component.submitForm();
            expect(component.mostrarResumenCompra).toHaveBeenCalledWith(3, new Date('2025-10-15'));

            fixture.detectChanges(); 

            const resumenElem = fixture.debugElement.query(By.css('.resumen-compra'));
            expect(resumenElem).toBeTruthy();

            const pTags = resumenElem.nativeElement.querySelectorAll('p');
            expect(pTags[0].textContent).toContain('Cantidad de entradas: 3');
            expect(pTags[1].textContent).toContain('Fecha de visita: 15/10/25');
        });

    });
});


