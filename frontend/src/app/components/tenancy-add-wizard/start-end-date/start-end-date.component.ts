import { Component } from '@angular/core';
import { NgbDate, NgbCalendar } from '@ng-bootstrap/ng-bootstrap';
import { TenancyAddConnector } from '../commons/tenancy-add-connector';
import { TenancyAddService } from 'src/app/services/tenancy-add.service';
import { ConvertToDateService } from 'src/app/services/date.service';

@Component({
  selector: 'app-start-end-date',
  templateUrl: './start-end-date.component.html',
  styleUrls: ['./start-end-date.component.css']
})
export class StartEndDateComponent extends TenancyAddConnector {
  hoveredDate: NgbDate;
  fromNgbDate: NgbDate;
  toNgbDate: NgbDate;

  constructor(private convertToDateService: ConvertToDateService,
              calendar: NgbCalendar, tenancyAddService: TenancyAddService) {
    super(tenancyAddService);
    this.fromNgbDate = calendar.getToday();
    this.toNgbDate = calendar.getNext(calendar.getToday(), 'd', 14);
  }

  protected alterBehaviourSubjectOnInit() {
    this.newTenancyMaker.tenancy.start_date = this.convertToDateService
      .fromNgbDate(this.fromNgbDate);
    this.newTenancyMaker.tenancy.end_date = this.convertToDateService
      .fromNgbDate(this.toNgbDate);
  }

  onDateSelection(date: NgbDate) {
    if (!this.fromNgbDate && !this.toNgbDate) {
      this.fromNgbDate = date;
    } else if (this.fromNgbDate && !this.toNgbDate &&
               date.after(this.fromNgbDate)) {
      this.toNgbDate = date;
    } else {
      this.toNgbDate = null;
      this.fromNgbDate = date;
    }

    if (this.fromNgbDate !== null) {
      this.newTenancyMaker.tenancy.start_date = this.convertToDateService
        .fromNgbDate(this.fromNgbDate);
    }
    if (this.toNgbDate !== null) {
      this.newTenancyMaker.tenancy.end_date = this.convertToDateService
        .fromNgbDate(this.toNgbDate);
    }
  }

  isHovered(date: NgbDate) {
    return this.fromNgbDate && !this.toNgbDate && this.hoveredDate &&
      date.after(this.fromNgbDate) && date.before(this.hoveredDate);
  }

  isInside(date: NgbDate) {
    return date.after(this.fromNgbDate) &&
      date.before(this.toNgbDate);
  }

  isRange(date: NgbDate) {
    return date.equals(this.fromNgbDate) || date.equals(this.toNgbDate) ||
      this.isInside(date) || this.isHovered(date);
  }
}
