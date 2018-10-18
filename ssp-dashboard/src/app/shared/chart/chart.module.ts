import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatTooltipModule } from '@angular/material/tooltip';

import { ChartComponent } from './chart.component';

@NgModule({
  imports: [
    CommonModule,
    
    MatButtonModule,
    MatCardModule,
    MatIconModule,
    MatTooltipModule
  ],
  declarations: [ChartComponent],
  exports: [ChartComponent]
})
export class ChartModule { }
