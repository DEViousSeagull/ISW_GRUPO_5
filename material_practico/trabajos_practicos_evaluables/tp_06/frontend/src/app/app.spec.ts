import { TestBed, ComponentFixture } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { AppComponent } from './app.component';
import { routes } from './app.routes';
import { By } from '@angular/platform-browser';
import { Location } from '@angular/common';

describe('AppComponent', () => {
    let fixture: ComponentFixture<AppComponent>;
    let router: Router;
    let location: Location;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [AppComponent, RouterTestingModule.withRoutes(routes)],
        }).compileComponents();

        router = TestBed.inject(Router);
        location = TestBed.inject(Location);
        fixture = TestBed.createComponent(AppComponent);
        router.initialNavigation(); // inicializa la navegación
    });

    it('should create the app', () => {
        const app = fixture.componentInstance;
        expect(app).toBeTruthy();
    });

    it('should navigate to /comprar-ticket when button is clicked', async () => {
        fixture.detectChanges();

        const button = fixture.debugElement.query(By.css('button'));
        button.nativeElement.click();

        // Espera a que Angular procese la navegación
        await fixture.isStable();

        expect(location.path()).toBe('/comprar-ticket');
    });
});
