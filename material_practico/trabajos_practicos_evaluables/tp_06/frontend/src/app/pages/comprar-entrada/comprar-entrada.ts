import { DatePipe } from '@angular/common';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormArray, AbstractControl, FormsModule, ReactiveFormsModule } from '@angular/forms';

@Component({
    selector: 'app-comprar-entrada',
    templateUrl: './comprar-entrada.html',
    styleUrls: ['./comprar-entrada.scss'],
    standalone: true,
    imports: [DatePipe, ReactiveFormsModule]
})
export class ComprarEntrada {
    formEntrada: FormGroup;
    resumenCompraVisible = false;
    cantidadEntradasResumen = 0;
    fechaResumen!: Date;

    // Example closed days
    diasCerrados = ['2025-10-19'];

    constructor(private fb: FormBuilder) {
        this.formEntrada = this.buildForm();
    }

    buildForm(): FormGroup {
        return this.fb.group({
            fechaVisita: ['', [Validators.required, this.fechaValida.bind(this)]],
            cantidadEntradas: [null, [Validators.required, Validators.min(1), Validators.max(10), Validators.pattern('^[0-9]+$')]],
            edades: this.fb.array([], this.edadesCoinciden.bind(this)),
            tipoPase: ['', Validators.required],
            formaPago: ['', Validators.required]
        });
    }

    get edades(): FormArray {
        return this.formEntrada.get('edades') as FormArray;
    }

    // Validator: Fecha no pasada y no cerrada
    fechaValida(control: AbstractControl) {
        const fecha = new Date(control.value);
        const hoy = new Date();
        hoy.setHours(0, 0, 0, 0);
        if (fecha < hoy) return { fechaPasada: true };
        if (this.diasCerrados.includes(control.value)) return { parqueCerrado: true };
        return null;
    }

    // Validator: cantidad de edades debe coincidir con cantidad de entradas
    edadesCoinciden(control: AbstractControl) {
        const cantidadEntradas = this.formEntrada?.get('cantidadEntradas')?.value || 0;
        const edades = (control as FormArray).controls || [];
        if (cantidadEntradas !== edades.length) return { edadesNoCoinciden: true };
        return null;
    }

    // Add edad input dynamically when cantidadEntradas changes
    actualizarEdades() {
        const cantidad = this.formEntrada.get('cantidadEntradas')?.value || 0;
        while (this.edades.length < cantidad) this.edades.push(this.fb.control('', [Validators.required, Validators.pattern('^[0-9]+$'), Validators.min(1)]));
        while (this.edades.length > cantidad) this.edades.removeAt(this.edades.length - 1);
    }

    submitForm() {
        if (this.formEntrada.invalid) return;

        this.cantidadEntradasResumen = this.formEntrada.get('cantidadEntradas')?.value;
        this.fechaResumen = new Date(this.formEntrada.get('fechaVisita')?.value);
        this.mostrarResumenCompra(this.cantidadEntradasResumen, this.fechaResumen);
    }

    mostrarResumenCompra(cantidad: number, fecha: Date) {
        this.resumenCompraVisible = true;
        // other logic if needed
    }
}
