import { Component, OnInit } from '@angular/core';
import { of, Subject, BehaviorSubject, merge, Observable } from 'rxjs';
import { flatMap, shareReplay, tap, map } from 'rxjs/operators';
import { ApiService } from '../core/api/api.service';
import { ParamsService } from '../core/params/params.service';

declare const moment: any;

@Component({
  selector: 'app-regioes',
  templateUrl: './regioes.component.html',
  styleUrls: ['./regioes.component.css']
})
export class RegioesComponent implements OnInit {

  private params$: Observable<any>;

  chartDistrictPie: any;

  chartDistrictSerial: any;
  chartDistrictSerialTrend: any;

  chartDistrictSerialSeasonal: any;
  chartDistrictSerialResid: any;

  year: string;
  modelType: Boolean;
  period: string;
  labelModelType: String;

  years: Array<any>;
  periods: Array<any>;

  private events: BehaviorSubject<any>;

  constructor(
    private apiService: ApiService,
    private paramsService: ParamsService
  ) {
    this.years = paramsService.years;
    this.year = this.years[1].value;
    this.modelType = true;
    this.labelModelType = "Modelo Aditivo";
    this.periods = paramsService.periods;
    this.period = this.periods[0].value;
    this.events = new BehaviorSubject({
      year: this.year,
      modelType: this.modelType,
      period: this.period
    });
    this.params$ = this.events.pipe(
      shareReplay(1),
      tap(params => {
        this.year = params.year;
        this.modelType = params.modelType;
        this.period = params.period
      }),
      map(params => {
        const { year, modelType, period } = params
        return {
          year, modelType, period
        }
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
      dataset: this.params$.pipe(flatMap((params) => {
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

    this.chartDistrictSerialTrend = {
      title: 'Tendência',
      subtitle: '',
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
      dataset: this.params$.pipe(flatMap((params) => {
        const model = params.modelType
        const year = params.year
        const periodicity = params.period
        if (params.year == 'all') {
          return this.apiService.fetchDistrictsTrends({ model, periodicity });
        } else {
          return this.apiService.fetchDistrictsTrends({ year, model, periodicity });
        }
      }))
    }

    this.chartDistrictSerialSeasonal = {
      title: 'Sazonalidade',
      subtitle: '',
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
      dataset: this.params$.pipe(flatMap((params) => {
        const model = params.modelType
        const year = params.year
        const periodicity = params.period
        if (params.year == 'all') {
          return this.apiService.fetchDistrictsSeasonal({ model, periodicity });
        } else {
          return this.apiService.fetchDistrictsSeasonal({ year, model, periodicity });
        }
      }))
    }

    this.chartDistrictSerialResid = {
      title: 'Ruídos',
      subtitle: '',
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
      dataset: this.params$.pipe(flatMap((params) => {
        const model = params.modelType
        const year = params.year
        const periodicity = params.period
        if (params.year == 'all') {
          return this.apiService.fetchDistrictsResids({ model, periodicity });
        } else {
          return this.apiService.fetchDistrictsResids({ year, model, periodicity });
        }
      }))
    }
  }

  onSelectYear(event) {
    this.labelModelType = `Modelo ${event.checked ? 'Aditivo' : 'Multiplicativo'}`;
    this.events.next({
      year: event.value,
      modelType: this.modelType,
      period: this.period
    });
  }

  onCheck(event) {
    this.labelModelType = `Modelo ${event.checked ? 'Aditivo' : 'Multiplicativo'}`;
    this.events.next({
      year: this.year,
      modelType: event.checked,
      period: this.period
    });
  }

  onSelectPeriod(event) {
    this.events.next({
      year: this.year,
      modelType: this.modelType,
      period: event.value,
    });
  }

}
