import { Router } from '@angular/router';
import { Component } from '@angular/core';

@Component({
    selector: 'app-home',
    standalone: true,
    imports: [],
    templateUrl: './home.html',
    styleUrls: ['./home.scss']
})
export class Home {
    constructor(private router: Router) { }
    onClick() {
        this.router.navigate(['comprar-entrada']);
    }
}
