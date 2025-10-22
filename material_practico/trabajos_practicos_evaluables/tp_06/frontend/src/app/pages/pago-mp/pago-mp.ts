import { Component, OnInit, OnDestroy, inject } from '@angular/core';
import { Router } from '@angular/router';
import { CurrencyPipe } from '@angular/common';
import { ComprasDb } from '../../services/compras/compras-db';
import { CompraDoc, PostBody } from '../../services/compras/compras-db';

@Component({
    selector: 'app-pago-mp',
    standalone: true,
    imports: [CurrencyPipe],
    templateUrl: './pago-mp.html',
    styleUrls: ['./pago-mp.scss']
})
export class PagoMp implements OnInit, OnDestroy {
    private router = inject(Router);
    private comprasDb = inject(ComprasDb);

    total = 0;
    postBody?: PostBody;

    paymentProcessing = false;
    paymentSuccess = false;

    compraCreada?: CompraDoc;

    secondsLeft = 3;
    private redirectTimeout?: any;
    private countdownInterval?: any;

    // 👉 handle de la nueva ventana para evitar bloqueadores
    private mailWin: Window | null = null;

    ngOnInit(): void {
        const state = history.state as { total?: number; postBody?: PostBody };
        if (!state?.total || !state?.postBody) {
            this.router.navigateByUrl('/');
            return;
        }
        this.total = state.total;
        this.postBody = state.postBody;
    }

    ngOnDestroy(): void {
        if (this.redirectTimeout) clearTimeout(this.redirectTimeout);
        if (this.countdownInterval) clearInterval(this.countdownInterval);
        this.mailWin = null;
    }

    async pagar() {
        if (this.paymentProcessing || !this.postBody) return;

        this.paymentProcessing = true;
        await new Promise(res => setTimeout(res, 2000)); // simulación pago
        this.paymentProcessing = false;
        this.paymentSuccess = true;

        try {
            const response = await this.comprasDb.post(this.postBody);
            this.compraCreada = response.compra;

            // Open Mail in a new tab
            const mailUrl = this.router.serializeUrl(this.router.createUrlTree(['/mail-box']));
            window.open(mailUrl, '_blank', 'noopener,noreferrer');

            // Refocus the current window to keep the user here
            window.focus();
            
            // ⏱️ start countdown & redirect this tab to detalle
            this.secondsLeft = 3;
            this.countdownInterval = setInterval(() => {
                this.secondsLeft--;
                if (this.secondsLeft <= 0 && this.countdownInterval) clearInterval(this.countdownInterval);
            }, 1000);

            this.redirectTimeout = setTimeout(() => {
                if (this.compraCreada) {
                    this.router.navigate(['/mis-compras', this.compraCreada.id]);
                } else {
                    this.router.navigateByUrl('/mis-compras');
                }
            }, 3000);

        } catch (err) {
            console.error('Error al crear compra:', err);
            alert('Hubo un error al procesar la compra.');
            this.paymentSuccess = false;
        }
    }


    cancelar() {
        if (this.paymentProcessing) return;
        this.router.navigateByUrl('/comprar-entrada');
    }
}
