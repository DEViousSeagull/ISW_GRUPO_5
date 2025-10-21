import { Component, signal } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';

interface AppUser {
    nombre: string,
    apellido: string,
    email: string
}



@Component({
    selector: 'app-root',
    templateUrl: './app.html',
    styleUrl: './app.scss',
    imports: [RouterOutlet, RouterModule],
})
export class App {
    protected mockUser: AppUser = {
        nombre: "Juan",
        apellido: "Pérez",
        email: "juan@example.com"
    }

}