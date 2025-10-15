import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { By } from '@angular/platform-browser';
import { Home } from './home';
import { Location } from '@angular/common';
import { Routes } from '@angular/router';
import { ComprarEntrada } from '../comprar-entrada/comprar-entrada';

describe('Home', () => {
    let component: Home;
    let fixture: ComponentFixture<Home>;
    let router: Router;
    let location: Location;

    const routes: Routes = [
        { path: 'comprar-entrada', component: ComprarEntrada }
    ];

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [Home, RouterTestingModule.withRoutes(routes)],
        }).compileComponents();

        router = TestBed.inject(Router);
        location = TestBed.inject(Location);

        fixture = TestBed.createComponent(Home);
        component = fixture.componentInstance;
        router.initialNavigation();
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should navigate to /comprar-entrada when button is clicked', async () => {
        const button = fixture.debugElement.query(By.css('button')).nativeElement;
        button.click();
        await fixture.whenStable(); 
        expect(location.path()).toBe('/comprar-entrada');
    });
});
