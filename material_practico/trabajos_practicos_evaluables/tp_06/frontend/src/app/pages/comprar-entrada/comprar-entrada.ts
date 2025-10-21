import { DatePipe, NgClass } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormArray, AbstractControl, ReactiveFormsModule } from '@angular/forms';
import { IntRangeDirective } from '../../directives/int-range.directive';
import { TipoEntrada, TiposPaseDb } from '../../services/tipos-pase/tipos-pase-db';

@Component({
    selector: 'app-comprar-entrada',
    templateUrl: './comprar-entrada.html',
    styleUrls: ['./comprar-entrada.scss'],
    standalone: true,
    imports: [DatePipe, ReactiveFormsModule, IntRangeDirective, NgClass]
})
export class ComprarEntrada implements OnInit {
    formEntrada: FormGroup;
    resumenCompraVisible = false;
    cantidadEntradasResumen = 0;
    fechaResumen!: Date;
    diasCerrados = ['2025-10-19'];

    tiposPase: TipoEntrada[] = [];

    constructor(
        private fb: FormBuilder,
        private tiposPaseDb: TiposPaseDb
    ) {
        this.formEntrada = this.buildForm();
    }

    async ngOnInit() {
        await this.loadTiposPase();
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
        const fecha = new Date(control.value);
        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0);
        if (fecha < hoy) return { fechaPasada: true };
        if (this.diasCerrados.includes(control.value)) return { parqueCerrado: true };
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

        while (this.visitantes.length < cantidad) {
            this.visitantes.push(
                this.fb.group({
                    edad: ['', [Validators.required, Validators.pattern('^[0-9]+$'), Validators.min(1)]],
                    tipoPase: ['', Validators.required]
                })
            );
        }

        while (this.visitantes.length > cantidad) {
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

    submitForm() {
        if (this.formEntrada.invalid) {
            this.formEntrada.markAllAsTouched();
            const firstError = document.querySelector('.ng-invalid');
            if (firstError) firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            return;
        }

        this.cantidadEntradasResumen = this.formEntrada.get('cantidadEntradas')?.value;
        this.fechaResumen = new Date(this.formEntrada.get('fechaVisita')?.value);
        this.resumenCompraVisible = true;

        console.log(this.formEntrada.value);
    }
}
