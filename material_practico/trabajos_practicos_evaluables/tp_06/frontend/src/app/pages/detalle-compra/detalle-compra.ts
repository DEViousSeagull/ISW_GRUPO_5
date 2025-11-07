import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe, CurrencyPipe } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { ComprasDb, CompraDoc, EntradaDoc } from '../../services/compras/compras-db';

@Component({
    selector: 'app-detalle-compra',
    templateUrl: './detalle-compra.html',
    styleUrls: ['./detalle-compra.scss'],
    standalone: true,
    imports: [CommonModule, DatePipe, CurrencyPipe]
})
export class DetalleCompra implements OnInit {
    compra?: CompraDoc;
    entradas: EntradaDoc[] = [];
    loading = true;
    error: string | null = null;

    constructor(private db: ComprasDb, private route: ActivatedRoute, private router: Router) { }

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

    abrirCorreo() {
        // Abrir la casilla de mail en otra pestaña, sin tomar el foco
        const mailUrl = this.router.serializeUrl(this.router.createUrlTree(['/mail-box']));
        window.open(mailUrl, '_blank', 'noopener,noreferrer');
        window.focus(); // mantené el foco en esta pestaña
    }

    formatFechaCompra(fechaIso?: string) {
        if (!fechaIso) return '';
        const fecha = new Date(fechaIso);
        // // Argentina is UTC-3
        fecha.setHours(fecha.getHours() - 3);
        return fecha;
    }
}
