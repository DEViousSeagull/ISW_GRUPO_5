import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ComprarEntrada } from './comprar-entrada';

describe('ComprarEntrada', () => {
  let component: ComprarEntrada;
  let fixture: ComponentFixture<ComprarEntrada>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ComprarEntrada]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ComprarEntrada);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
