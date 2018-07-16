import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

import { ApiService } from './api/api.service';
import { AnalyticsDataParserService, AnalyticsSettingsService } from './analytics/analytics.service';
import { DateService } from './date/date.service';

@NgModule({
  imports: [
    CommonModule,
    HttpClientModule
  ],
  declarations: [],
  providers: [
    ApiService,
    AnalyticsDataParserService,
    AnalyticsSettingsService,
    DateService
  ]
})
export class CoreModule { }
