import { TestBed, ComponentFixture } from '@angular/core/testing';
import { HomeComponent } from './home';
import { RouterTestingModule } from '@angular/router/testing';
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import { By } from '@angular/platform-browser';

describe('HomeComponent', () => {
    let fixture: ComponentFixture<HomeComponent>;
    let router: Router;
    let location: Location;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [
                HomeComponent,
                RouterTestingModule.withRoutes([
                    { path: 'comprar-ticket', component: HomeComponent }, // stub component
                ]),
            ],
        }).compileComponents();

        router = TestBed.inject(Router);
        location = TestBed.inject(Location);
        fixture = TestBed.createComponent(HomeComponent);

        router.initialNavigation();
    });

    it('should create the home component', () => {
        const component = fixture.componentInstance;
        expect(component).toBeTruthy();
    });

    it('should navigate to /comprar-ticket when button is clicked', async () => {
        fixture.detectChanges();

        const button = fixture.debugElement.query(By.css('button'));
        button.nativeElement.click();

        await fixture.isStable(); // espera a que Angular termine la navegación

        expect(location.path()).toBe('/comprar-ticket');
    });
});
