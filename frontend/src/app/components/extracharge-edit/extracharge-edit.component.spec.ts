import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExtrachargeEditComponent } from './extracharge-edit.component';

describe('ExtrachargeEditComponent', () => {
  let component: ExtrachargeEditComponent;
  let fixture: ComponentFixture<ExtrachargeEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExtrachargeEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExtrachargeEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
