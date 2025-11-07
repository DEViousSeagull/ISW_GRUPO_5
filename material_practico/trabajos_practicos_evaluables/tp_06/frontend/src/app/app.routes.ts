import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { ComprarEntrada } from './pages/comprar-entrada/comprar-entrada';
import { DetalleCompra } from './pages/detalle-compra/detalle-compra';
import { MisCompras } from './pages/mis-compras/mis-compras';
import { PagoMp } from './pages/pago-mp/pago-mp';
import { MainLayout } from './pages/main-layout/main-layout';
import { BlankLayout } from './pages/blank-layout/blank-layout';
import { MailBox } from './pages/mail-box/mail-box';

export const routes: Routes = [
    {
        path: '',
        component: MainLayout,
        children: [
            { path: '', component: Home, pathMatch: 'full' },
            { path: 'comprar-entrada', component: ComprarEntrada },
            { path: 'mis-compras', component: MisCompras },
            { path: 'mis-compras/:id', component: DetalleCompra },
        ],
    },

    {
        path: '',
        component: BlankLayout,
        children: [
            { path: 'pago-mp', component: PagoMp },
            { path: 'mail-box', component: MailBox },
        ],
    },

    // Fallback
    { path: '**', redirectTo: '' },
];
