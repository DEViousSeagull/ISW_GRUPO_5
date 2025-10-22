import { Component, OnInit } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { CommonModule, DatePipe, CurrencyPipe } from '@angular/common';
import { ComprasDb, CompraDoc } from '../../services/compras/compras-db';

@Component({
    selector: 'app-mis-compras',
    templateUrl: './mis-compras.html',
    styleUrls: ['./mis-compras.scss'],
    standalone: true,
    imports: [CommonModule, RouterModule, DatePipe, CurrencyPipe]
})
export class MisCompras implements OnInit {
    compras: CompraDoc[] = [];
    loading = true;
    error: string | null = null;

    constructor(private db: ComprasDb, private router: Router) { }

    async ngOnInit() {
        try {
            this.compras = await this.db.getAll();
        } catch (err) {
            console.error(err);
            this.error = 'No se pudieron cargar las compras.';
        } finally {
            this.loading = false;
        }
    }

    irAMisEntradas(compraId: number) {
        this.router.navigate(['/mis-compras', compraId]);
    }
}
