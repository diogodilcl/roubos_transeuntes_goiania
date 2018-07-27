import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';
import { shareReplay } from '../../../../node_modules/rxjs/operators';

declare const moment: any;

@Injectable()
export class ParamsService {

  get years(): Array<any> {
    return [].concat([
      { value: '2017', viewValue: '2017' },
      { value: '2016', viewValue: '2016' },
      { value: '2015', viewValue: '2015' },
      { value: 'all', viewValue: 'Todos' }
    ]);
  }

  get periods(): Array<any> {
    return [].concat([
      { value: 'monthly', viewValue: 'Mensal' },
      { value: 'quarter', viewValue: 'Trimestral' },
      { value: 'semester', viewValue: 'Semestral' }
    ]);
  }

  get localities(): Array<any> {
    return [].concat([
      { value: 'neighborhood', viewValue: 'Bairro' },
      { value: 'district', viewValue: 'Região' },
      { value: 'city', viewValue: 'Municipio' }
    ]);
  }

}
