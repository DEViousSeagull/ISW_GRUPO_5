import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { ComprarEntrada } from './pages/comprar-entrada/comprar-entrada';
import { DetalleCompra } from './pages/detalle-compra/detalle-compra';
import { MisCompras } from './pages/mis-compras/mis-compras';

export const routes: Routes = [
    {
        path: '',
        component: Home,
        pathMatch: 'full',
    },
    {
        path: 'comprar-entrada',
        component: ComprarEntrada,
    },
    {
        path: 'mis-compras',
        component: MisCompras,
    },
    {
        path: 'mis-compras/:id',
        component: DetalleCompra,
    },
    {
        path: '**',
        redirectTo: '', // fallback to home
    },
];
