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

    private comprasDb = inject(ComprasDb);
    private router = inject(Router);

    loading = false;
    error?: string;
    compras: CompraDoc[] = [];

    async ngOnInit() {
        this.loading = true;
        try {
            this.compras = await this.comprasDb.getAll();
            // Orden opcional: más recientes primero por fecha (ISO)
            // this.compras.sort((a, b) => b.fecha.localeCompare(a.fecha));
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
}
