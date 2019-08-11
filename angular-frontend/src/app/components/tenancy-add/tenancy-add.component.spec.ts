import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TenancyAddComponent } from './tenancy-add.component';

describe('TenancyAddComponent', () => {
  let component: TenancyAddComponent;
  let fixture: ComponentFixture<TenancyAddComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TenancyAddComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TenancyAddComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
