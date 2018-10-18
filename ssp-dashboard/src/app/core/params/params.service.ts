import { Injectable } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';
import { shareReplay } from '../../../../node_modules/rxjs/operators';

declare const moment: any;

@Injectable()
export class ParamsService {

  get years(): Array<any> {
    return [].concat([
      { value: '2018', viewValue: '2018' },
      { value: '2017', viewValue: '2017' },
      { value: '2016', viewValue: '2016' },
      { value: '2015', viewValue: '2015' },
      { value: '2014', viewValue: '2014' },
      { value: '2013', viewValue: '2013' },
      { value: '2012', viewValue: '2012' },
      { value: '2011', viewValue: '2011' },
      { value: 'all', viewValue: 'Todos' }
    ]);
  }

  get periods(): Array<any> {
    return [].concat([
      { value: 'monthly', viewValue: 'Mensal' },
      { value: 'quarter', viewValue: 'Trimestral' },
      { value: 'semester', viewValue: 'Semestral' },
      // { value: 'year', viewValue: 'Anual' }
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
