import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TenantNamesComponent } from './tenant-names.component';

describe('TenantNamesComponent', () => {
  let component: TenantNamesComponent;
  let fixture: ComponentFixture<TenantNamesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TenantNamesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TenantNamesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
