import { Component, OnInit, inject } from '@angular/core';
import { DatePipe, CurrencyPipe } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { ComprasDb, CompraDoc } from '../../services/compras/compras-db';

@Component({
    selector: 'app-mail-box',
    standalone: true,
    imports: [DatePipe, CurrencyPipe, RouterModule],
    templateUrl: './mail-box.html',
    styleUrls: ['./mail-box.scss']
})
export class MailBox implements OnInit {



    loading = false;
    error?: string;
    compras: CompraDoc[] = [];

    constructor(private comprasDb: ComprasDb, private router: Router,) {

    }

    async ngOnInit() {
        this.loading = true;
        try {
            this.compras = await this.comprasDb.getAll();

            this.compras.sort((a, b) => b.id - a.id);

        } catch (e) {
            console.error(e);
            this.error = 'No se pudieron cargar los correos.';
        } finally {
            this.loading = false;
        }
    }

    abrirDetalle(id: number) {
        this.router.navigate(['/mis-compras', id]);
    }

    formatFechaCompra(fechaIso?: string) {
        if (!fechaIso) return '';
        const fecha = new Date(fechaIso);
        // // Argentina is UTC-3
        fecha.setHours(fecha.getHours() - 3);
        return fecha;
    }
}
