import { Injectable } from '@angular/core';

declare const moment: any;

@Injectable()
export class DateService {

  constructor() { }

  last(quantity: number = 1, unit: string = 'month') {
    return moment().subtract(quantity, unit).toDate();
  }

  format(value: Date, format: string = 'YYYY-MM-DD') {
    return moment(value).format(format);
  }

  isBefore(date: Date, dateToCompare: Date = new Date()) {
    return moment(date).isBefore(dateToCompare);
  }

}
