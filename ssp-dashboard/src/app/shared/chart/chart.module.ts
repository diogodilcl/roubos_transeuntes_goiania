import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';

import { ChartComponent } from './chart.component';

@NgModule({
  imports: [
    CommonModule,
    
    MatCardModule,
    MatIconModule
  ],
  declarations: [ChartComponent],
  exports: [ChartComponent]
})
export class ChartModule { }
