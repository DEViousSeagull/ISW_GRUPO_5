import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { ComprarEntrada } from './pages/comprar-entrada/comprar-entrada';

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
        path: '**',
        redirectTo: '', // fallback to home
    },
];
