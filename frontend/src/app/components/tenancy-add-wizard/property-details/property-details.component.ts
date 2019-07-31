import { Component } from '@angular/core';
import { TenancyAddConnector } from '../commons/tenancy-add-connector';
import { TenancyAddService } from 'src/app/services/tenancy-add.service';

@Component({
  selector: 'app-property-details',
  templateUrl: './property-details.component.html',
  styleUrls: ['./property-details.component.css']
})
export class PropertyDetailsComponent extends TenancyAddConnector {
  rentTypeList = {
    '0': '-- Please select a rent type --',
    'Whole Property': 'Whole Property',
    'Private Room': 'Private Room'
  };

  constructor(tenancyAddService: TenancyAddService) {
    super(tenancyAddService);
  }

  alterBehaviourSubjectOnInit(){
    this.setRentType('0');
  }

  setRentType(setRentTypeName) {
    this.newTenancyMaker.tenancy.rent_type = setRentTypeName
  }

  getSelectedRentTypeValue() {
    return this.rentTypeList[this.newTenancyMaker.tenancy.rent_type]
  }
}
