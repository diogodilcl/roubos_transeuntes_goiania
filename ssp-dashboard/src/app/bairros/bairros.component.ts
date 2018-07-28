import { Component, OnInit } from '@angular/core';
import { flatMap, shareReplay, tap } from 'rxjs/operators';
import { BehaviorSubject, Subject, Observable } from 'rxjs';
import { ApiService } from '../core/api/api.service';
import { ParamsService } from '../core/params/params.service';

declare const moment: any;

@Component({
  selector: 'app-bairros',
  templateUrl: './bairros.component.html',
  styleUrls: ['./bairros.component.css']
})
export class BairrosComponent implements OnInit {

  private params$: Observable<any>;

  chartBairroTrend : any

  chartBairroSeasonal : any
  chartBairroResid : any

  chartNeighborhoodSerial: any
  chartNeighborhoodPie: any
  
  year: string;
  modelType: Boolean;
  labelModelType: String;

  years: Array<any>;

  private events: BehaviorSubject<any>;
  
  constructor(
    private apiService: ApiService,
    private paramsService: ParamsService
  ) {
    this.years = paramsService.years;
    this.year = this.years[0].value
    this.modelType = true;
    this.labelModelType = "Modelo Aditivo";
    this.events = new BehaviorSubject({
      year: this.year,
      modelType: this.modelType
    });
    this.params$ = this.events.pipe(
      shareReplay(1),
      tap(params => {
        this.year = params.year;
        this.modelType = params.modelType
      })
    );
  }

  ngOnInit() {
    this.chartNeighborhoodSerial = {
      title: 'Quantitativo Local',
      subtitle: 'Crimes por bairros',
      type: 'serial',
      dataset: this.params$.pipe(
        flatMap((params) => {
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
        const model = params.modelType
        const year = params.year
        return this.apiService.fetchNeighborhoodsTrends({ year, model});
      }))
    }
    this.chartBairroSeasonal = {
      title: 'Sazonalidade',
      subtitle: '',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const model = params.modelType
        const year = params.year
        return this.apiService.fetchNeighborhoodsSeasonal({ year, model});
      }))
    }
    this.chartBairroResid = {
      title: 'Ruídos',
      subtitle: '',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const model = params.modelType
        const year = params.year
        return this.apiService.fetchNeighborhoodsResids({ year, model});
      }))
    }
  }

  onSelectYear(event) {
    this.events.next({
      year: this.year,
      labelModelType: "Modelo " + (event.checked ? "Multiplicativo" : "Aditivo"),
      modelType: event.checked
    });
  }

  onCheck(event) {
    this.modelType = event.checked;
    this.events.next({
      year: this.year,
      labelModelType: "Modelo " + (event.checked ? "Multiplicativo" : "Aditivo"),
      modelType: event.checked
    });
  }

}
