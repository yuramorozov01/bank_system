import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtmWithdrawPageComponent } from './atm-withdraw-page.component';

describe('AtmWithdrawPageComponent', () => {
  let component: AtmWithdrawPageComponent;
  let fixture: ComponentFixture<AtmWithdrawPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AtmWithdrawPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AtmWithdrawPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
