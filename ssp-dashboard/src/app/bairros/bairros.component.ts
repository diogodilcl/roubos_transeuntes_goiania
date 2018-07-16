import { Component, OnInit } from '@angular/core';
import { flatMap } from 'rxjs/operators';
import { BehaviorSubject, Subject } from 'rxjs';
import { ApiService } from '../core/api/api.service';

declare const moment: any;

@Component({
  selector: 'app-bairros',
  templateUrl: './bairros.component.html',
  styleUrls: ['./bairros.component.css']
})
export class BairrosComponent implements OnInit {

  years: Array<any> = [
    { value: '2017', viewValue: '2017'},
    { value: '2016', viewValue: '2016'},
    { value: '2015', viewValue: '2015'}
  ];
  chartBairroTrend : any
  chartBairroSeasonal : any
  chartBairroResid : any
  chartNeighborhoodSerial: any
  chartNeighborhoodPie: any
  params$ : Subject<any>

  constructor(
    private apiService: ApiService
  ) {
    this.params$ = new BehaviorSubject({
      year: this.years[0].value
    });
  }

  ngOnInit() {
    this.chartNeighborhoodSerial = {
      title: 'Quantitativo Local',
      subtitle: 'Crimes por bairros',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const start = moment().year(params.year).month(0).dayOfYear(1).toDate();
        const end = moment().year(params.year).month(0).dayOfYear(365).toDate();
        return this.apiService.fetchNeighborhoods({ start, end });
      }))
    }
    this.chartNeighborhoodPie = {
      title: 'Percentual Local',
      subtitle: '-',
      type: 'pie',
      dataset: this.params$.pipe(flatMap((params) => {
        const start = moment().year(params.year).month(0).dayOfYear(1).toDate();
        const end = moment().year(params.year).month(0).dayOfYear(365).toDate();
        return this.apiService.fetchNeighborhoods({ start, end });
      }))
    }
    this.chartBairroTrend = {
      title: 'Tendência',
      subtitle: '',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const year = params.year
        return this.apiService.fetchNeighborhoodsTrends({ year});
      }))
    }
    this.chartBairroSeasonal = {
      title: 'Sazonalidade',
      subtitle: '',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const year = params.year
        return this.apiService.fetchNeighborhoodsSeasonal({ year});
      }))
    }
    this.chartBairroResid = {
      title: 'Ruídos',
      subtitle: '',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const year = params.year
        return this.apiService.fetchNeighborhoodsResids({ year});
      }))
    }
  }

  onSelectYear(event) {
    this.params$.next({
      year: event.value
    });
  }

}
