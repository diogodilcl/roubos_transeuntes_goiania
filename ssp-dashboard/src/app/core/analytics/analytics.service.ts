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
    this.map.set('column', this.columnDataParser);
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
        date: label.date,
        dashLength: label.prediction ? 8 : 0
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

  columnDataParser(result: any): any {
    const titles = [], filteredData = result.data.map(d => {
      titles.push(d.label);
      return d;
    });
    const data = result.labels.map((label, index) => {
      const obj = {
        date: label.date,
        dashLength: label.prediction ? 8 : 0
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

}

@Injectable({
  providedIn: 'root'
})
export class AnalyticsSettingsService {

  private map: Map<string, (dataset: any, options?: any) => any>;

  constructor(
    private analyticsDataParserService: AnalyticsDataParserService
  ) {
    this.map = new Map();
    this.map.set('pie', this.pieSetting);
    this.map.set('serial', this.serialSetting);
    this.map.set('bar', this.barSetting);
    this.map.set('column', this.columnSetting);
  }

  getChartSettings(type: string, dataset: any, options?: any): any {
    return this.map.get(type)(dataset, options);
  }

  pieSetting = (dataset: any): any => {
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

  serialSetting = (dataset: any, options: any): any => {
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
      if (options.hasBars) {
        graphs.push({
          'alphaField': 'alpha',
          'balloonText': '[[value]]',
          'dashLengthField': 'dashLength',
          'fillAlphas': 0.7,
          'legendPeriodValueText': 'total: [[value.sum]]',
          'legendValueText': '[[value]]',
          'title': title,
          'type': 'column',
          'valueField': title,
          'valueAxis': `axis_${title}`
        });
      } else {
        graphs.push({
          'valueAxis': `axis_${title}`,
          'balloonText': `[[title]]: <b>[[value]]</b>`,
          'bulletBorderThickness': 1,
          'hideBulletsCount': 30,
          'lineThickness': 2,
          'title': title,
          'valueField': title,
          'fillAlphas': 0,
          'animationPlayed': true,
          'dashLengthField': 'dashLength',
          'bullet': 'round'
        });
      }
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
        'parseDates': options ? !!options.parseDates : true
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
      'dataProvider': data,
      'chartScrollbar': {
        'enabled': true
      },
      'export': {
        'enabled': true,
        'position': 'bottom-right',
        'pageMargins': {
          'bottom': 30,
          'right': 40
        }
      },
    });
  }

  barSetting = (dataset: any): any => {

  }

  columnSetting = (datase: any): any => {

    return Object.assign({}, {
      'type': 'serial',
      'categoryField': 'category',
      'startDuration': 1,
      'categoryAxis': {
        'gridPosition': 'start'
      },
      'trendLines': [],
      'graphs': [
        {
          'balloonText': '[[title]] of [[category]]:[[value]]',
          'fillAlphas': 1,
          'id': 'AmGraph-1',
          'title': 'graph 1',
          'type': 'column',
          'valueField': 'column-1'
        },
        {
          'balloonText': '[[title]] of [[category]]:[[value]]',
          'fillAlphas': 1,
          'id': 'AmGraph-2',
          'title': 'graph 2',
          'type': 'column',
          'valueField': 'column-2'
        }
      ],
      'guides': [],
      'valueAxes': [
        {
          'id': 'ValueAxis-1',
          'title': 'Axis title'
        }
      ],
      'allLabels': [],
      'balloon': {},
      'legend': {
        'enabled': true,
        'useGraphSettings': true
      },
      'titles': [
        {
          'id': 'Title-1',
          'size': 15,
          'text': 'Chart Title'
        }
      ],
      'dataProvider': [
        {
          'category': 'category 1',
          'column-1': 8,
          'column-2': 5
        },
        {
          'category': 'category 2',
          'column-1': 6,
          'column-2': 7
        },
        {
          'category': 'category 3',
          'column-1': 2,
          'column-2': 3
        }
      ]
    })
  }

}
