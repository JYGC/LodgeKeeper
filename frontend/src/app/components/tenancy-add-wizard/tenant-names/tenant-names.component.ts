import { Component } from '@angular/core';
import { TenancyAddConnector } from '../commons/tenancy-add-connector';
import { TenancyAddService } from 'src/app/services/tenancy-add.service';

@Component({
  selector: 'app-tenant-names',
  templateUrl: './tenant-names.component.html',
  styleUrls: ['./tenant-names.component.css']
})
export class TenantNamesComponent extends TenancyAddConnector {
  constructor(tenancyAddService: TenancyAddService) {
    super(tenancyAddService);
  }
}
