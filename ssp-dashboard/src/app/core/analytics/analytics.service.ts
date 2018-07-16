import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AnalyticsDataParserService {

  private map: Map<string, (dataset: any) => any>;

  constructor() {
    this.map = new Map();
    this.map.set('pie', this.pieDataParser);
    this.map.set('serial', this.serialDataParser);
    this.map.set('bar', this.barDataParser);
  }

  pieDataParser(dataset: any): any {
    return dataset.data.map(d => ({
      title: d.label,
      value: d.total
    }));
  }

  serialDataParser(result: any): any {
    const titles = [], filteredData = result.data.map(d => {
      titles.push(d.label);
      return d;
    });
    const data = result.labels.map((label, index) => {
      const obj = {
        date: label
      };
      filteredData.forEach(d => {
        obj[d.label] = d.values[index];
      });
      return obj;
    });
    return {
      titles: titles,
      data: data
    };
  }

  barDataParser(dataset: any): any {

  }

}

@Injectable({
  providedIn: 'root'
})
export class AnalyticsSettingsService {

  private map: Map<string, (dataset: any) => any>;

  constructor(
    private analyticsDataParserService: AnalyticsDataParserService
  ) {
    this.map = new Map();
    this.map.set('pie', this.pieSetting.bind(this));
    this.map.set('serial', this.serialSetting.bind(this));
    this.map.set('bar', this.barSetting.bind(this));
  }

  getChartSettings(type: string, dataset: any): any {
    return this.map.get(type)(dataset);
  }

  pieSetting(dataset: any): any {
    return Object.assign({}, {
      'type': 'pie',
      'fontFamily': 'Roboto, \'Helvetica Neue\',sans-serif',
      'balloonText': '[[title]]<br><span style=\'font-size: 14px\'><b>[[value]]</b> ([[percents]]%)</span>',
      'gradientType': 'linear',
      'theme': 'light',
      'innerRadius': 0,
      'sequencedAnimation': false,
      'startDuration': 0,
      'labelText': '[[percents]]%',
      'titleField': 'title',
      'valueField': 'value',
      'legend': {
        'enabled': true,
        'align': 'center',
        'markerType': 'circle',
        'valueAlign': 'left'
      },
      'language': 'pt',
      'dataProvider': this.analyticsDataParserService.pieDataParser(dataset)
    })
  }

  serialSetting(dataset: any): any {
    const valueAxes = [], graphs = [];
    const { titles, data } = this.analyticsDataParserService.serialDataParser(dataset);
    titles.forEach((title, index) => {
      valueAxes.push({
        'id': title,
        'axisColor': '#FF6600',
        'axisThickness': 2,
        'axisAlpha': 1,
        'position': 'left'
      });
      graphs.push({
        'valueAxis': `axis_${title}`,
        'balloonText': `[[title]]: <b>[[value]]</b>`,
        'bulletBorderThickness': 1,
        'hideBulletsCount': 30,
        'lineThickness': 2,
        'title': title,
        'valueField': title,
        'fillAlphas': 0,
        'animationPlayed': true
      });
    });
    return Object.assign({}, {
      'type': 'serial',
      'fontFamily': 'Roboto, \'Helvetica Neue\',sans-serif',
      'startDuration': 0,
      'theme': 'light',
      'categoryField': 'date',
      'dataDateFormat': 'YYYY-MM',
      'categoryAxis': {
        'minPeriod': 'MM',
        'parseDates': true
      },
      'chartCursor': {
        'enabled': true,
        'categoryBalloonDateFormat': 'MMM YYYY'
      },
      'graphs': graphs,
      'valueAxes': valueAxes,
      'legend': {
        'enabled': true,
        'useGraphSettings': true
      },
      'language': 'pt',
      'dataProvider': data
    });
  }

  barSetting(dataset: any): any {

  }

}
