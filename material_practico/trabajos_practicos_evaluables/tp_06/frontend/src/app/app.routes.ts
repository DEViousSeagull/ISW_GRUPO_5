import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home';
import { ComprarEntradaComponent } from './pages/comprar-entrada/comprar-entrada';


export const routes: Routes = [
    { path: '', component: HomeComponent },
    { path: 'comprar-ticket', component: ComprarEntradaComponent },
];