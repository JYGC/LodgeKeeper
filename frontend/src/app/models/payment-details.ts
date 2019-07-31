export interface IPaymentDetails {
  payment_method: string;
  description: string;
}

export class BankDetails implements IPaymentDetails {
  payment_method: string = 'Bank Transfer';
  bank_name: string;
  account_name: string;
  bsb_number: string;
  account_number: string;
  description: string;
}

export class PayPalDetails implements IPaymentDetails {
  payment_method: string = 'PayPal';
  email: string;
  reason: string;
  message: string;
  description: string;
}

export class CashDetails implements IPaymentDetails {
  payment_method: string = 'Cash';
  description: string;
}

export class PaymentMethodSelector {
  private validPaymentDetails = [
    new BankDetails(),
    new PayPalDetails(),
    new CashDetails()
  ];
  selectedPaymentMethod: string;

  constructor(public paymentDetailsObjs = new Map<number, IPaymentDetails>()) {
    for (let i = 0; i < this.validPaymentDetails.length; i++) {
      this.paymentDetailsObjs[
        this.validPaymentDetails[i].payment_method
      ] = this.validPaymentDetails[i].payment_method;
    }
  }

  changeSelectedPaymentMethod(name: string) {
    this.selectedPaymentMethod = name;
  }

  getSelectedPaymentMethod(): IPaymentDetails {
    return this.paymentDetailsObjs[this.selectedPaymentMethod]
  }
}