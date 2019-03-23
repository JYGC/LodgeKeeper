import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TenancyEditComponent } from './tenancy-edit.component';

describe('TenancyEditComponent', () => {
  let component: TenancyEditComponent;
  let fixture: ComponentFixture<TenancyEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TenancyEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TenancyEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
