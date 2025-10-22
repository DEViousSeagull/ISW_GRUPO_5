import { Component, signal } from '@angular/core';
import { RouterModule, RouterOutlet } from '@angular/router';

interface AppUser {
    nombre: string,
    apellido: string,
    email: string,
    id: number
}

export const MOCK_USER: AppUser = {
    nombre: "Juan",
    apellido: "Pérez",
    email: "juan@example.com",
    id: 1
}

@Component({
    selector: 'app-root',
    standalone: true,
    templateUrl: './app.html',
    styleUrls: ['./app.scss'],
    imports: [RouterOutlet, RouterModule],
})
export class App {
    protected mockUser: AppUser = MOCK_USER;

}