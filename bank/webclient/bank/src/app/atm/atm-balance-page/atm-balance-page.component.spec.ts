import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtmBalancePageComponent } from './atm-balance-page.component';

describe('AtmBalancePageComponent', () => {
  let component: AtmBalancePageComponent;
  let fixture: ComponentFixture<AtmBalancePageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AtmBalancePageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AtmBalancePageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
