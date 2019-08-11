import { Component } from '@angular/core';
import { TenancyAddConnector } from '../commons/tenancy-add-connector';
import { TenancyAddService } from 'src/app/services/tenancy-add.service';

@Component({
  selector: 'app-rent-payment',
  templateUrl: './rent-payment.component.html',
  styleUrls: ['./rent-payment.component.css']
})
export class RentPaymentComponent extends TenancyAddConnector {
  paymentTermsList = {
    '0': '-- Please select your payment terms --',
    'Per week': 'Per week',
    'Per fortnight': 'Per fortnight',
    'Per month': 'Per month'
  }

  paymentMethodsList = {
    '0': '-- Please select your payment method --'
  };

  constructor(tenancyAddService: TenancyAddService) {
    super(tenancyAddService);
  }

  alterBehaviourSubjectOnInit() {
    for(let paymentDetailName in this.newTenancyMaker.paymentSelector.paymentDetailsObjs) {
      this.paymentMethodsList[paymentDetailName] = this.newTenancyMaker
        .paymentSelector.paymentDetailsObjs[paymentDetailName];
    }
    this.setPaymentType('0');
    this.setPaymentMethods('0');
  }

  setPaymentType(paymentTermName) {
    this.newTenancyMaker.tenancy.payment_terms = paymentTermName
  }

  getCurPaymentTypeValue() {
    return this.paymentTermsList[this.newTenancyMaker.tenancy.payment_terms];
  }

  setPaymentMethods(paymentMethodName) {
    this.newTenancyMaker.paymentSelector
      .selectedPaymentMethod = paymentMethodName;
  }

  getCurPaymentMethodValue(): string {
    return this.paymentMethodsList[
      this.newTenancyMaker.paymentSelector.selectedPaymentMethod
    ];
  }
}
