import { Component } from '@angular/core';
import { RouterModule } from "@angular/router";
import { MOCK_USER } from '../../app';

@Component({
    selector: 'app-main-layout',
    standalone: true,
    imports: [RouterModule],
    templateUrl: './main-layout.html',
    styleUrls: ['./main-layout.scss']
})
export class MainLayout {
    protected mockUser = MOCK_USER;

}
