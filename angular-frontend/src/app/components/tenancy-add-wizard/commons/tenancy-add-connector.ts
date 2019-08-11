import { OnInit } from '@angular/core';
import { NewTenancyMaker } from 'src/app/models/tenancy';
import { TenancyAddService } from 'src/app/services/tenancy-add.service';

export class TenancyAddConnector implements OnInit {
  protected newTenancyMaker: NewTenancyMaker;
  
  constructor(private tenancyAddService: TenancyAddService) {
    this.newTenancyMaker = new NewTenancyMaker();
  }

  ngOnInit() {
    this.tenancyAddService.currentMessage.subscribe(
      message => this.newTenancyMaker = message
    );
    this.alterBehaviourSubjectOnInit();
  }

  protected alterBehaviourSubjectOnInit() { }
}
