import { Component, signal } from '@angular/core';
import { Router, RouterOutlet } from '@angular/router';

@Component({
    selector: 'app-root',
    imports: [RouterOutlet],
    templateUrl: './app.html',
    styleUrl: './app.scss'
})
export class AppComponent {
    protected readonly title = signal('eco-harmony-park');

    constructor(private router: Router) { }

    goToBuyTicket() {
        this.router.navigate(['/comprar-ticket']);
    }
}
