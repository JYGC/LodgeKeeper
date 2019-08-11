import { IPaymentDetails, PaymentMethodSelector } from './payment-details';

export class Tenancy {
  public start_date: Date;
  public end_date: Date;
  public address: string;
  public room_name: string;
  public rent_type: number;
  public payment_terms: number;
  
  constructor(){ }
}


export class NewTenancy {
  constructor(public tenancy: Tenancy, public tenants: string[],
              public payment_details: IPaymentDetails,
              public notifications: string[]) { }
}

export class NewTenancyMaker {
  constructor(
    public tenancy: Tenancy = new Tenancy(), 
    private tenantFieldIndex = 0,
    public tenantFields: any[] = [],
    public paymentSelector: PaymentMethodSelector = new PaymentMethodSelector(),
    private notificationFieldIndex = 0,
    public notificationFields: any[] = []
  ) { }
  
  private addTextField(fieldList: any[], key, value) {
    fieldList.push({
      key: key,//'tenant' + fieldList.length.toString(),
      value: value
    });
  }

  addTenant() {
    this.addTextField(this.tenantFields, 'tenant' + this.tenantFieldIndex, '');
    this.tenantFieldIndex++;
  }

  deleteTenant(i) {
    this.tenantFields.splice(i, 1);
  }

  addNotification() {
    this.addTextField(this.notificationFields,
                      'notification' + this.notificationFieldIndex, 7);
    this.notificationFieldIndex++;
  }

  deleteNotification(i) {
    this.notificationFields.splice(i, 1);
  }

  setNotification(i, value) {
    this.notificationFields[i].value = parseInt(value);
  }

  private getValueFromField(fieldList) {
    return fieldList.map(function (field) {
      return field.value;
    });
  }

  makeNewTenancy() {
    return new NewTenancy(this.tenancy,
                          this.getValueFromField(this.tenantFields),
                          this.paymentSelector.getSelectedPaymentMethod(),
                          this.getValueFromField(this.notificationFields));
  }
}
