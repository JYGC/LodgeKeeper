import { Component } from '@angular/core';
import { TenancyAddConnector } from '../commons/tenancy-add-connector';
import { TenancyAddService } from 'src/app/services/tenancy-add.service';

@Component({
  selector: 'app-notification-scheduling',
  templateUrl: './notification-scheduling.component.html',
  styleUrls: ['./notification-scheduling.component.css']
})
export class NotificationSchedulingComponent extends TenancyAddConnector {
  days = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9 , 10, 11, 12, 13, 14];
  
  constructor(tenancyAddService: TenancyAddService) {
    super(tenancyAddService);
  }
}
