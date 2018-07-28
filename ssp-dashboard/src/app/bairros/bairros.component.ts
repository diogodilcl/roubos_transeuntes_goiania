import { Component, OnInit } from '@angular/core';
import { flatMap, shareReplay, tap, map } from 'rxjs/operators';
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

  chartBairroTrend: any

  chartBairroSeasonal: any
  chartBairroResid: any

  chartNeighborhoodSerial: any
  chartNeighborhoodPie: any

  bairros: Array<any>;
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
    this.year = this.years[0].value;
    this.bairros = [];
    this.modelType = true;
    this.labelModelType = "Modelo Aditivo";
    this.events = new BehaviorSubject({
      year: this.year,
      modelType: this.modelType,
      bairros: this.bairros
    });
    this.params$ = this.events.pipe(
      shareReplay(1),
      tap(params => {
        this.bairros = params.bairros;
        this.year = params.year;
        this.modelType = params.modelType
      }),
      map(params => {
        const { year, modelType } = params
        return {
          year, modelType, bairros: params.bairros.map(b => b.id)
        }
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
          if (params.year == 'all') {
            return this.apiService.fetchNeighborhoods({ ids: params.bairros });
          } else {
            const start = moment().year(params.year).month(0).dayOfYear(1).toDate();
            const end = moment().year(params.year).month(0).dayOfYear(365).toDate();
            return this.apiService.fetchNeighborhoods({ start, end, ids: params.bairros });
          }
        }))
    }
    this.chartNeighborhoodPie = {
      title: 'Percentual Local',
      subtitle: '-',
      type: 'pie',
      dataset: this.params$.pipe(flatMap((params) => {
        if (params.year == 'all') {
          return this.apiService.fetchNeighborhoods({ ids: params.bairros });
        } else {
          const start = moment().year(params.year).month(0).dayOfYear(1).toDate();
          const end = moment().year(params.year).month(0).dayOfYear(365).toDate();
          return this.apiService.fetchNeighborhoods({ start, end, ids: params.bairros });
        }
      }))
    }
    this.chartBairroTrend = {
      title: 'Tendência',
      subtitle: '',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const model = params.modelType
        const year = params.year
        if (params.year == 'all') {
          return this.apiService.fetchNeighborhoodsTrends({ model, ids: params.bairros });
        } else {
          return this.apiService.fetchNeighborhoodsTrends({ year, model, ids: params.bairros });
        }
      }))
    }
    this.chartBairroSeasonal = {
      title: 'Sazonalidade',
      subtitle: '',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const model = params.modelType
        const year = params.year
        if (params.year == 'all') {
          return this.apiService.fetchNeighborhoodsSeasonal({ model, ids: params.bairros });
        } else {
          return this.apiService.fetchNeighborhoodsSeasonal({ year, model, ids: params.bairros });
        }
      }))
    }
    this.chartBairroResid = {
      title: 'Ruídos',
      subtitle: '',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const model = params.modelType
        const year = params.year
        if (params.year == 'all') {
          return this.apiService.fetchNeighborhoodsResids({ model, ids: params.bairros });
        } else {
          return this.apiService.fetchNeighborhoodsResids({ year, model, ids: params.bairros });
        }
      }))
    }
  }

  onSelectYear(event) {
    this.labelModelType = `Modelo ${event.checked ? 'Aditivo' : 'Multiplicativo'}`;
    this.events.next({
      year: event.value,
      modelType: this.modelType,
      bairros: this.bairros
    });
  }

  onCheck(event) {
    this.labelModelType = `Modelo ${event.checked ? 'Aditivo' : 'Multiplicativo'}`;
    this.events.next({
      year: this.year,
      modelType: event.checked,
      bairros: this.bairros
    });
  }

  onBairrosChanged(bairros) {
    this.events.next({
      year: this.year,
      modelType: this.modelType,
      bairros: bairros
    });
  }

}
