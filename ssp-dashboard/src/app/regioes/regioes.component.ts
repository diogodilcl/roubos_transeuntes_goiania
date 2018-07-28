import { Component, OnInit } from '@angular/core';
import { Subject, BehaviorSubject, merge, Observable } from 'rxjs';
import { flatMap, shareReplay, tap } from 'rxjs/operators';
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
    this.chartDistrictPie = {
      title: 'Percentual regional',
      subtitle: '-',
      type: 'pie',
      dataset: this.params$.pipe(
        flatMap((params) => {
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
        const model = params.modelType
        const year = params.year
        return this.apiService.fetchDistrictsTrends({ year, model });
      }))
    }
    this.chartDistrictSerialSeasonal = {
      title: 'Sazonalidade',
      subtitle: '',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const model = params.modelType
        const year = params.year
        return this.apiService.fetchDistrictsSeasonal({ year, model });
      }))
    }
    this.chartDistrictSerialResid = {
      title: 'Ruídos',
      subtitle: '',
      type: 'serial',
      dataset: this.params$.pipe(flatMap((params) => {
        const model = params.modelType
        const year = params.year
        return this.apiService.fetchDistrictsResids({ year, model });
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
