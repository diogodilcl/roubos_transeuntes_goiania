import { Component, OnInit } from '@angular/core';
import { of, Observable, BehaviorSubject } from 'rxjs';

import { flatMap, shareReplay, tap } from 'rxjs/operators';

import { ApiService } from '../core/api/api.service';
import { ParamsService } from '../core/params/params.service';

declare const moment: any;

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  private params$: Observable<any>;

  chartCitySerial: any;

  chartDistrictPie: any;
  chartDistrictSerial: any;

  chartNeighborhoodPie: any;
  chartNeighborhoodSerial: any;

  year: string;
  period: string;
  locality: string;


  years: Array<any>;
  periods: Array<any>;
  localities: Array<any>;

  private events: BehaviorSubject<any>;

  constructor(
    private apiService: ApiService,
    private paramsService: ParamsService
  ) {
    this.years = paramsService.years;
    this.periods = paramsService.periods;
    this.period = this.periods[0].value
    this.year = this.years[1].value
    this.events = new BehaviorSubject({
      year: this.year,
      period: this.period
    });
    this.params$ = this.events.pipe(
      shareReplay(1),
      tap(params => {
        this.year = params.year;
        this.period = params.period
      })
    );
  }

  ngOnInit() {
    this.chartDistrictPie = {
      title: 'Percentual regional',
      subtitle: '-',
      type: 'pie',
      dataset: this.params$.pipe(
        flatMap((params) => {
          const periodicity = params.period
          if (params.year == 'all') {
            return this.apiService.fetchDistricts({ periodicity });
          } else {
            const start = moment().year(params.year).month(0).dayOfYear(1).toDate();
            const end = moment().year(params.year).month(0).dayOfYear(365).toDate();
            return this.apiService.fetchDistricts({ start, end, periodicity });
          }
        }))
    }

    this.chartNeighborhoodPie = {
      title: 'Percentual Local',
      subtitle: '-',
      type: 'pie',
      dataset: this.params$.pipe(
        flatMap((params) => {
          const periodicity = params.period
          if (params.year == 'all') {
            return this.apiService.fetchNeighborhoods({ periodicity });
          } else {
            const start = moment().year(params.year).month(0).dayOfYear(1).toDate();
            const end = moment().year(params.year).month(0).dayOfYear(365).toDate();
            return this.apiService.fetchNeighborhoods({ start, end, periodicity });
          }
        }))
    }
    
    this.chartCitySerial = {
      title: 'Quantitativo de Crimes',
      subtitle: 'Crimes em Goiânia através do tempo',
      type: 'serial',
      options: this.params$.pipe(
        flatMap((params) => {
          if (params.period !== 'monthly') {
            return of({
              parseDates: false
            });
          }
          return of({
            parseDates: true
          });
        })),
      dataset: this.params$.pipe(
        flatMap((params) => {
          const periodicity = params.period
          if (params.year == 'all') {
            return this.apiService.fetchCities({ periodicity });
          } else {
            const start = moment().year(params.year).month(0).dayOfYear(1).toDate();
            const end = moment().year(params.year).month(0).dayOfYear(365).toDate();
            return this.apiService.fetchCities({ start, end, periodicity });
          }
        }))
    }
    this.chartDistrictSerial = {
      title: 'Quantitativo Regional',
      subtitle: 'Crimes por regiões',
      type: 'serial',
      options: this.params$.pipe(
        flatMap((params) => {
          if (params.period !== 'monthly') {
            return of({
              parseDates: false
            });
          }
          return of({
            parseDates: true
          });
        })),
      dataset: this.params$.pipe(
        flatMap((params) => {
          const periodicity = params.period
          if (params.year == 'all') {
            return this.apiService.fetchDistricts({ periodicity });
          } else {
            const start = moment().year(params.year).month(0).dayOfYear(1).toDate();
            const end = moment().year(params.year).month(0).dayOfYear(365).toDate();
            return this.apiService.fetchDistricts({ start, end, periodicity });
          }
        }))
    }
    this.chartNeighborhoodSerial = {
      title: 'Quantitativo Local',
      subtitle: 'Crimes por bairros',
      type: 'serial',
      options: this.params$.pipe(
        flatMap((params) => {
          if (params.period !== 'monthly') {
            return of({
              parseDates: false
            });
          }
          return of({
            parseDates: true,
          });
        })),
      dataset: this.params$.pipe(
        flatMap((params) => {
          const periodicity = params.period
          if (params.year == 'all') {
            return this.apiService.fetchNeighborhoods({ periodicity });
          } else {
            const start = moment().year(params.year).month(0).dayOfYear(1).toDate();
            const end = moment().year(params.year).month(0).dayOfYear(365).toDate();
            return this.apiService.fetchNeighborhoods({ start, end, periodicity });
          }
        }))
    }
  }

  onSelectYear(event) {
    this.events.next({
      year: event.value,
      period: this.period
    });
  }

  onSelectPeriod(event) {
    this.events.next({
      year: this.year,
      period: event.value
    });
  }

}
