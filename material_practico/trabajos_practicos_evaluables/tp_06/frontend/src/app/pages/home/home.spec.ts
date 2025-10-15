import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { By } from '@angular/platform-browser';
import { Home } from './home';

describe('Home', () => {
    let component: Home;
    let fixture: ComponentFixture<Home>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [Home, RouterTestingModule],
        }).compileComponents();

        fixture = TestBed.createComponent(Home);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });

    it('should have a button to navigate to comprar-tickets', () => {
        const button = fixture.debugElement.query(By.css('button'));
        expect(button).toBeTruthy();
        expect(button.nativeElement.textContent).toContain('Comprar Entrada');
    });
});
