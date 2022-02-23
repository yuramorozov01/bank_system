import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AtmSiteLayoutComponent } from './atm-site-layout.component';

describe('AtmSiteLayoutComponent', () => {
  let component: AtmSiteLayoutComponent;
  let fixture: ComponentFixture<AtmSiteLayoutComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AtmSiteLayoutComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AtmSiteLayoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
