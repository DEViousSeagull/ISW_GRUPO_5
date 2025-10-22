import { Component } from '@angular/core';
import { RouterModule } from "@angular/router";

@Component({
    selector: 'app-blank-layout',
    standalone: true,
    imports: [RouterModule],
    templateUrl: './blank-layout.html',
    styleUrls: ['./blank-layout.scss']
})
export class BlankLayout {}
