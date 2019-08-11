import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TenantbillEditComponent } from './tenantbill-edit.component';

describe('TenantbillEditComponent', () => {
  let component: TenantbillEditComponent;
  let fixture: ComponentFixture<TenantbillEditComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TenantbillEditComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TenantbillEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
