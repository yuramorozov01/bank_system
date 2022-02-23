import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtmLoginPageComponent } from './atm-login-page.component';

describe('AtmLoginPageComponent', () => {
  let component: AtmLoginPageComponent;
  let fixture: ComponentFixture<AtmLoginPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AtmLoginPageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AtmLoginPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
