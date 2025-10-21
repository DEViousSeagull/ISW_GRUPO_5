import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe, CurrencyPipe } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { ComprasDb, CompraDoc, EntradaDoc } from '../../services/compras/compras-db';

@Component({
    selector: 'app-mis-entradas',
    templateUrl: './mis-entradas.html',
    styleUrls: ['./mis-entradas.scss'],
    standalone: true,
    imports: [CommonModule, DatePipe, CurrencyPipe]
})
export class MisEntradas implements OnInit {
    compra?: CompraDoc;
    entradas: EntradaDoc[] = [];
    loading = true;
    error: string | null = null;

    constructor(private db: ComprasDb, private route: ActivatedRoute) { }

    async ngOnInit() {
        const idParam = this.route.snapshot.paramMap.get('id');
        if (!idParam) {
            this.error = 'No se especificó la compra.';
            this.loading = false;
            return;
        }

        const id = Number(idParam);
        if (isNaN(id)) {
            this.error = 'ID inválido.';
            this.loading = false;
            return;
        }

        try {
            this.compra = await this.db.getById(id);
            if (!this.compra) {
                this.error = `No se encontró la compra con id ${id}.`;
            } else {
                this.entradas = this.compra.entradas;
            }
        } catch (err) {
            console.error(err);
            this.error = 'Error al cargar la compra.';
        } finally {
            this.loading = false;
        }
    }
}
