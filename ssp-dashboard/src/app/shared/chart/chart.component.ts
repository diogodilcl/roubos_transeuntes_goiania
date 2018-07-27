import { Component, OnInit, OnDestroy, AfterViewInit, Input } from '@angular/core';
import { Observable } from 'rxjs';

import AmChart from 'amcharts/AmChart';
import { AnalyticsSettingsService } from '../../core/analytics/analytics.service';

declare const AmCharts: any;

@Component({
  selector: 'app-chart',
  templateUrl: './chart.component.html',
  styleUrls: ['./chart.component.css']
})
export class ChartComponent implements OnInit, OnDestroy, AfterViewInit {

  @Input() title: string;
  @Input() subtitle: string;
  @Input() type: string;
  @Input() dataset: Observable<any>;
  @Input() options: Observable<any>;

  id: string;
  chart: AmChart;
  currentOptions: any;

  constructor(private analyticsSettingsService: AnalyticsSettingsService) {
    this.id = `chart_${Math.random().toString(18).substr(2)}`;
  }

  ngOnInit() {

  }

  ngAfterViewInit(): void {
    if (this.options) {
      this.options.subscribe(options => this.currentOptions = options);
    }
    this.dataset.subscribe(data => {
      this.chart = AmCharts.makeChart(this.id, this.analyticsSettingsService.getChartSettings(this.type, data, this.currentOptions));
    });
  }

  ngOnDestroy(): void {
    if (this.chart) {
      this.chart.clear();
    }
  }

}
