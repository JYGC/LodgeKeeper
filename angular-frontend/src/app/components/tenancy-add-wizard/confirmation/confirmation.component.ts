import { Component, OnInit } from '@angular/core';
import { TenancyAddConnector } from '../commons/tenancy-add-connector';
import { TenancyAddService } from 'src/app/services/tenancy-add.service';

@Component({
  selector: 'app-confirmation',
  templateUrl: './confirmation.component.html',
  styleUrls: ['./confirmation.component.css']
})
export class ConfirmationComponent extends TenancyAddConnector {
  constructor(tenancyAddService: TenancyAddService) {
    super(tenancyAddService);
  }
}
