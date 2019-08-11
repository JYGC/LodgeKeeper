import { Injectable, Output } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { NewTenancyMaker } from '../models/tenancy';

@Injectable({
  providedIn: 'root'
})
export class TenancyAddService {
  private messageSource = new BehaviorSubject(new NewTenancyMaker());
  currentMessage = this.messageSource.asObservable();

  constructor() { }
}
