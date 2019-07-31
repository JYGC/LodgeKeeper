import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NotificationSchedulingComponent } from './notification-scheduling.component';

describe('NotificationSchedulingComponent', () => {
  let component: NotificationSchedulingComponent;
  let fixture: ComponentFixture<NotificationSchedulingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NotificationSchedulingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NotificationSchedulingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
