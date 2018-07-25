import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

declare const moment: any;

@Injectable()
export class ParamsService {

  
  private modelType: boolean

  private years: Array<any> = [
    { value: '2017', viewValue: '2017' },
    { value: '2016', viewValue: '2016' },
    { value: '2015', viewValue: '2015' },
    { value: 'all', viewValue: 'Todos' }
  ];


  private periods: Array<any> = [
    { value: 'monthly', viewValue: 'Mensal' },
    { value: 'quarterly', viewValue: 'Trimestral' },
    { value: 'semesterly', viewValue: 'Semestral' },
    { value: 'annually', viewValue: 'Anual' }
  ];

  private localities: Array<any> = [
    { value: 'neighborhood', viewValue: 'Bairro' },
    { value: 'district', viewValue: 'Região' },
    { value: 'city', viewValue: 'Municipio' }
  ];

  private yearsObservable = new Observable((observer) => {
    observer.next(this.years);
    observer.complete()
  })

  private periodsObservable = new Observable((observer) => {
    observer.next(this.periods);
    observer.complete()
  })

  private localitiesObservable = new Observable((observer) => {
    observer.next(this.localities);
    observer.complete()
  })

  constructor() { }

  getLocalities(): Observable<any> {
    return this.localitiesObservable;
  }
  getPeriods(): Observable<any> {
    return this.periodsObservable;
  }
  getYears(): Observable<any> {
    return this.yearsObservable;
  }
}
