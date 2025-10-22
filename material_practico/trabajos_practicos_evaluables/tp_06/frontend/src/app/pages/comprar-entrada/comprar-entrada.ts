import { CurrencyPipe, DatePipe, NgClass } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormArray, AbstractControl, ReactiveFormsModule } from '@angular/forms';
import { IntRangeDirective } from '../../directives/int-range.directive';
import { TipoEntrada, TiposPaseDb } from '../../services/tipos-pase/tipos-pase-db';
import { CompraDoc, ComprasDb, PostBody } from '../../services/compras/compras-db';
import { FormaPago, FormasPagoDb } from '../../services/formas-pago/formas-pago-db';
import { Router } from '@angular/router';

@Component({
    selector: 'app-comprar-entrada',
    templateUrl: './comprar-entrada.html',
    styleUrls: ['./comprar-entrada.scss'],
    standalone: true,
    imports: [DatePipe, ReactiveFormsModule, IntRangeDirective, NgClass, CurrencyPipe]
})
export class ComprarEntrada implements OnInit {
    formEntrada: FormGroup;


    confirmModalVisible = false;
    detalleCompra?: CompraDoc;

    tiposPase: TipoEntrada[] = [];
    formasPago: FormaPago[] = [];

    constructor(
        private fb: FormBuilder,
        private tiposPaseDb: TiposPaseDb,
        private formasPagoDb: FormasPagoDb,
        private comprasDb: ComprasDb,
        private router: Router
    ) {
        this.formEntrada = this.buildForm();
    }

    async ngOnInit() {
        await this.loadTiposPase();
        await this.loadFormasPago();
    }

    private async loadFormasPago() {
        try {
            this.formasPago = await this.formasPagoDb.getAll();
        } catch (error) {
            console.error('Error cargando formas de pago:', error);
        }
    }

    private async loadTiposPase() {
        try {
            this.tiposPase = await this.tiposPaseDb.getAll();
        } catch (error) {
            console.error('Error cargando tipos de pase:', error);
        }
    }

    buildForm(): FormGroup {
        return this.fb.group({
            fechaVisita: ['', [Validators.required, this.fechaValida.bind(this)]],
            cantidadEntradas: [
                null,
                [Validators.required, Validators.min(1), Validators.max(10), Validators.pattern('^[0-9]+$')]
            ],
            visitantes: this.fb.array([], this.visitantesCoinciden.bind(this)),
            formaPago: ['', Validators.required]
        });
    }

    get visitantes(): FormArray {
        return this.formEntrada.get('visitantes') as FormArray;
    }

    fechaValida(control: AbstractControl) {
        const fecha = new Date(control.value + 'T00:00:00');
        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0);

        // Check if date is in the past
        if (fecha < hoy) return { fechaPasada: true };

        // Check if Monday (0 = Monday, ...)
        if (fecha.getDay() === 0) return { parqueCerrado: true };

        // Check if Christmas or New Year's
        const month = fecha.getMonth() + 1; // getMonth() 0-11
        const day = fecha.getDate(); // empieza en 0

        console.log("MONTH", month, "DAY", day)
        if ((month === 12 && day === 25) || (month === 1 && day === 1)) {
            return { parqueCerrado: true };
        }

        return null;
    }
    visitantesCoinciden(control: AbstractControl) {
        const cantidadEntradas = this.formEntrada?.get('cantidadEntradas')?.value || 0;
        const visitantes = (control as FormArray).controls || [];
        if (cantidadEntradas !== visitantes.length) return { visitantesNoCoinciden: true };
        return null;
    }

    actualizarVisitantes() {
        const cantidad = this.formEntrada.get('cantidadEntradas')?.value || 0;
        const maxEntradas = 10;

        const finalCantidad = Math.min(cantidad, maxEntradas); // cap at 10

        // Add missing controls
        while (this.visitantes.length < finalCantidad) {
            this.visitantes.push(
                this.fb.group({
                    edad: ['', [Validators.required, Validators.pattern('^[0-9]+$'), Validators.min(0), Validators.max(100)]],
                    tipoPase: ['', Validators.required]
                })
            );
        }

        // Remove extra controls
        while (this.visitantes.length > finalCantidad) {
            this.visitantes.removeAt(this.visitantes.length - 1);
        }
    }


    control(name: string) {
        return this.formEntrada.get(name);
    }

    isInvalid(name: string) {
        const c = this.control(name);
        return !!c && c.invalid && (c.touched || c.dirty);
    }

    hasError(name: string, err: string) {
        const c = this.control(name);
        return !!c?.errors?.[err];
    }

    edadCtrl(i: number) {
        return (this.visitantes.at(i) as FormGroup).get('edad');
    }
    paseCtrl(i: number) {
        return (this.visitantes.at(i) as FormGroup).get('tipoPase');
    }

    edadInvalid(i: number) {
        const c = this.edadCtrl(i);
        return c?.invalid && (c?.touched || c?.dirty);
    }
    edadHasError(i: number, err: string) {
        return !!this.edadCtrl(i)?.errors?.[err];
    }

    paseInvalid(i: number) {
        const c = this.paseCtrl(i);
        return c?.invalid && (c?.touched || c?.dirty);
    }

    private buildPostBody(): PostBody {
        const fecha = this.formEntrada.get('fechaVisita')?.value;
        const cantidadEntradas = this.formEntrada.get('cantidadEntradas')?.value;
        const formaPagoId = Number(this.formEntrada.get('formaPago')?.value); // ensure number

        const entradas = this.visitantes.controls.map(ctrl => ({
            edad: Number(ctrl.get('edad')?.value),
            tipo_entrada: { id: Number(ctrl.get('tipoPase')?.value) }
        }));

        return {
            fecha,
            cantidad_entradas: cantidadEntradas,
            usuario: { id: 1 },
            forma_pago: { id: formaPagoId },
            entradas
        };
    }



    async submitForm() {
        if (this.formEntrada.invalid) {
            this.formEntrada.markAllAsTouched();
            const firstError = document.querySelector('.ng-invalid');
            if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return;
        }

        // this.cantidadEntradasResumen = this.formEntrada.get('cantidadEntradas')?.value;
        // this.fechaResumen = new Date(this.formEntrada.get('fechaVisita')?.value);
        // this.resumenCompraVisible = true;

        // console.log(this.formEntrada.value);

        const postBody = this.buildPostBody();
        // console.log(postBody);



        try {
            const response = await this.comprasDb.post(postBody);
            console.log('Compra creada:', response.compra);

            this.detalleCompra = response.compra;
            this.confirmModalVisible = true;

        } catch (err) {
            console.error('Error al crear compra:', err);
            alert('Hubo un error al procesar la compra.');
        }

    }


    continuarComprando() {
        this.confirmModalVisible = false;
        this.formEntrada.reset();
        this.visitantes.clear();
    }

    async verDetalle(id: number) {

        await this.router.navigate(['/mis-compras', id]);

        this.confirmModalVisible = false;
        this.formEntrada.reset();
        this.visitantes.clear();
    }

}
