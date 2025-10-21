import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { ComprarEntrada } from './pages/comprar-entrada/comprar-entrada';
import { MisEntradas } from './pages/mis-entradas/mis-entradas';
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
        path: 'mis-entradas/:id',
        component: MisEntradas,
    },
    {
        path: '**',
        redirectTo: '', // fallback to home
    },
];
