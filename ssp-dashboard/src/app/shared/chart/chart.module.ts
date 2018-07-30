import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';

import { ChartComponent } from './chart.component';

@NgModule({
  imports: [
    CommonModule,
    
    MatButtonModule,
    MatCardModule,
    MatIconModule
  ],
  declarations: [ChartComponent],
  exports: [ChartComponent]
})
export class ChartModule { }
