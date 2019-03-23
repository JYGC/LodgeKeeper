import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ExtrachargeAddComponent } from './extracharge-add.component';

describe('ExtrachargeAddComponent', () => {
  let component: ExtrachargeAddComponent;
  let fixture: ComponentFixture<ExtrachargeAddComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ExtrachargeAddComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ExtrachargeAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
