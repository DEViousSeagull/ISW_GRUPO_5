import { Router } from '@angular/router';
import { Component } from '@angular/core';

@Component({
    selector: 'app-home',
    imports: [],
    templateUrl: './home.html',
    styleUrl: './home.scss'
})
export class Home {
    constructor(private router: Router) { }
    onClick() {
        console.log("COMPRAR ENTRADAS")
        this.router.navigate(['comprar-entrada']);
    }
}
