import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { FormControl } from '@angular/forms';

import { Observable, Subject } from 'rxjs';
import { debounceTime, flatMap } from 'rxjs/operators';

import { ApiService } from '../../core/api/api.service';

@Component({
  selector: 'app-bairro-search',
  templateUrl: './bairro-search.component.html',
  styleUrls: ['./bairro-search.component.css']
})
export class BairroSearchComponent implements OnInit {

  @Output() bairrosChanged: EventEmitter<any>;

  bairroSelectInput: FormControl;
  bairros$: Observable<any>;
  bairrosSelected: Array<any>;

  private bairrosEvent: Subject<any>;

  constructor(
    private apiService: ApiService
  ) {
    this.bairrosChanged = new EventEmitter();
    this.bairrosSelected = [];
    this.bairrosEvent = new Subject();
    this.bairros$ = this.bairrosEvent.pipe(
      flatMap(params => this.apiService.searchNeighborhoods(params))
    )
  }

  ngOnInit() {
    this.bairroSelectInput = new FormControl();
    this.bairroSelectInput.valueChanges
      .pipe(
        debounceTime(350)
      )
      .subscribe(name => this.bairrosEvent.next({ name }))
  }

  onBairroSelected(bairro) {
    (!this.bairrosSelected.find(b => b.id === bairro.id)) && this.bairrosSelected.push(bairro);
    this.bairrosChanged.emit(this.bairrosSelected);
  }

  onRemoveBairro(bairro) {
    this.bairrosSelected = this.bairrosSelected.filter(b => b.id !== bairro.id);
    this.bairrosChanged.emit(this.bairrosSelected);
  }

}
