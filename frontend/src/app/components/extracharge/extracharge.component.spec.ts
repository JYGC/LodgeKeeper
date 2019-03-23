import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExtrachargeComponent } from './extracharge.component';

describe('ExtrachargeComponent', () => {
  let component: ExtrachargeComponent;
  let fixture: ComponentFixture<ExtrachargeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExtrachargeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExtrachargeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
