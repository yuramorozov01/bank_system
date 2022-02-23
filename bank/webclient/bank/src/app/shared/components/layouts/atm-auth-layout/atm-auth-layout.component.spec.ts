import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtmAuthLayoutComponent } from './atm-auth-layout.component';

describe('AtmAuthLayoutComponent', () => {
  let component: AtmAuthLayoutComponent;
  let fixture: ComponentFixture<AtmAuthLayoutComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AtmAuthLayoutComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AtmAuthLayoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
