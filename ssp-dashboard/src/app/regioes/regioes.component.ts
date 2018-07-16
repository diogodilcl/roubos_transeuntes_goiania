import { Component, OnInit } from '@angular/core';
import { Subject, BehaviorSubject, merge } from 'rxjs';

import { flatMap } from 'rxjs/operators';

import { ApiService } from '../core/api/api.service';

declare const moment: any;

@Component({
  selector: 'app-regioes',
  templateUrl: './regioes.component.html',
  styleUrls: ['./regioes.component.css']
})
export class RegioesComponent implements OnInit {

  private params$: Subject<any>;

  years: Array<any> = [
    { value: '2017', viewValue: '2017' },
    { value: '2016', viewValue: '2016' },
    { value: '2015', viewValue: '2015' }
  ];
  chartDistrictPie: any;
  chartDistrictSerial: any;
  chartDistrictSerialTrend: any;
  chartDistrictSerialSeasonal: any;
  chartDistrictSerialResid: any;

  constructor(
    private apiService: ApiService
  ) {
    this.params$ = new BehaviorSubject({
      year: this.years[0].value
    });
  }

  ngOnInit() {
    this.chartDistrictPie = {
      title: 'Percentual regional',
      subtitle: '-',
      type: 'pie',
      dataset: this.params$.pipe(flatMap((params) => {
        const start = moment().year(params.year).month(0).dayOfYear(1).toDate();
        const end = moment().year(params.year).month(0).dayOfYear(365).toDate();
        return this.apiService.fetchDistricts({ start, end });
      }))
    }
    this.chartDistrictSerial = {
      title: 'Quantitativo Regional',
      subtitle: 'Crimes por regiões',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const start = moment().year(params.year).month(0).dayOfYear(1).toDate();
        const end = moment().year(params.year).month(0).dayOfYear(365).toDate();
        return this.apiService.fetchDistricts({ start, end });
      }))
    }

    this.chartDistrictSerialTrend = {
      title: 'Tendência',
      subtitle: '',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const year = params.year
        return this.apiService.fetchDistrictsTrends({ year });
      }))
    }

    this.chartDistrictSerialSeasonal = {
      title: 'Sazonalidade',
      subtitle: '',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const year = params.year
        return this.apiService.fetchDistrictsSeasonal({ year });
      }))
    }

    this.chartDistrictSerialResid = {
      title: 'Ruídos',
      subtitle: '',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const year = params.year
        return this.apiService.fetchDistrictsResids({ year });
      }))
    }
  }

}
