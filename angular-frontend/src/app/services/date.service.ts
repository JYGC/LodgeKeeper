import { Injectable } from '@angular/core';
import { NgbDate } from '@ng-bootstrap/ng-bootstrap';

@Injectable({
  providedIn: 'root'
})
export class ConvertToDateService {
  constructor() { }

  fromNgbDate(ngbDate: NgbDate) {
    return new Date(ngbDate.year, ngbDate.month - 1, ngbDate.day - 1);
  }
}
