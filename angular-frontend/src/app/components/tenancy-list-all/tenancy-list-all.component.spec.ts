import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TenancyListAllComponent } from './tenancy-list-all.component';

describe('TenancyListAllComponent', () => {
  let component: TenancyListAllComponent;
  let fixture: ComponentFixture<TenancyListAllComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TenancyListAllComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TenancyListAllComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
