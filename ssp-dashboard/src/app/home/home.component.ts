import { Component, OnInit } from '@angular/core';
import { Subject, BehaviorSubject, merge } from 'rxjs';

import { flatMap } from 'rxjs/operators';

import { ApiService } from '../core/api/api.service';
import { ParamsService } from '../core/params/params.service';

declare const moment: any;

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  private params$: Subject<any>;

  chartCitySerial: any;

  chartDistrictPie: any;
  chartDistrictSerial: any;

  chartNeighborhoodPie: any;
  chartNeighborhoodSerial: any;

  year: string;
  perioid: string;
  locality: string;
  modelType: boolean;
  labelModelType: String;

  years: Array<any>;
  periods: Array<any>;
  localities: Array<any>;




  constructor(private apiService: ApiService, private paramsService: ParamsService) {

    this.modelType = true;
    this.labelModelType = "Modelo Multiplicativo";

    paramsService.getLocalities().subscribe((localities) => {
      this.localities = localities;
    });
    paramsService.getYears().subscribe((years) => {
      this.years = years;
      this.year = this.years[0].value
      this.params$ = new BehaviorSubject({
        year: this.year
      });
    });
    paramsService.getPeriods().subscribe((periods) => {
      this.periods = periods;
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
    this.chartCitySerial = {
      title: 'Quantitativo de Crimes',
      subtitle: 'Crimes em Goiânia através do tempo',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const start = moment().year(params.year).month(0).dayOfYear(1).toDate();
        const end = moment().year(params.year).month(0).dayOfYear(365).toDate();
        return this.apiService.fetchCities({ start, end });
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
  }

  onSelectYear(event) {
    this.params$.next({
      year: event.value
    });
  }

  onSelectPeriod(event) {
    // this.params$.next({
    //   year: event.value
    // });
  }

  onCheck(event) {
    this.modelType = event.checked;
    this.labelModelType = "Modelo " + (this.modelType ? "Multiplicativo" : "Aditivo");
  }


}
