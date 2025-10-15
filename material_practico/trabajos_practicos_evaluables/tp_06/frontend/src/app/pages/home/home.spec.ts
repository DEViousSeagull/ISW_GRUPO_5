import { ComponentFixture, TestBed } from '@angular/core/testing';
import { provideRouter, Router } from '@angular/router';
import { By } from '@angular/platform-browser';
import { Home } from './home';
import { Location } from '@angular/common';
import { provideLocationMocks } from '@angular/common/testing';
import { routes } from '../../app.routes';

describe('Home', () => {
    let component: Home;
    let fixture: ComponentFixture<Home>;
    let router: Router;
    let location: Location;



    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [Home],
            providers: [provideRouter(routes), provideLocationMocks()]

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
