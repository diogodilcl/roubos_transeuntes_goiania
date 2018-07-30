import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';

import { MatInputModule } from '@angular/material/input';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatChipsModule } from '@angular/material/chips';

import { BairroSearchComponent } from './bairro-search.component';

@NgModule({
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatInputModule,
    MatAutocompleteModule,
    MatChipsModule
  ],
  declarations: [BairroSearchComponent],
  exports: [BairroSearchComponent]
})
export class BairroSearchModule { }
