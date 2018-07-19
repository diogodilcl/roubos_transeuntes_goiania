import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { DateService } from '../date/date.service';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private static readonly BASE_URL = 'http://tcc-env.fmpyp2b6w6.sa-east-1.elasticbeanstalk.com/v1';
  //private static readonly BASE_URL = 'http://localhost:5000/v1';

  constructor(
    private http: HttpClient,
    private dateService: DateService
  ) { }

  fetchCities(parameters) {
    return this.http.get(`${ApiService.BASE_URL}/thefts/cities`, { params: this.parseParameters(parameters) });
  }

  fetchDistricts(parameters) {
    return this.http.get(`${ApiService.BASE_URL}/thefts/districts`, { params: this.parseParameters(parameters) });
  }

  fetchNeighborhoods(parameters) {
    return this.http.get(`${ApiService.BASE_URL}/thefts/neighborhoods`, { params: this.parseParameters(parameters) });
  }

  fetchDistrictsTrends(parameters) {
    return this.http.get(`${ApiService.BASE_URL}/thefts/districts/trend`, { params: this.parseParameters(parameters) });
  }

  fetchNeighborhoodsTrends(parameters) {
    return this.http.get(`${ApiService.BASE_URL}/thefts/neighborhoods/trend`, { params: this.parseParameters(parameters) });
  }

  fetchDistrictsResids(parameters) {
    return this.http.get(`${ApiService.BASE_URL}/thefts/districts/resid`, { params: this.parseParameters(parameters) });
  }

  fetchNeighborhoodsResids(parameters) {
    return this.http.get(`${ApiService.BASE_URL}/thefts/neighborhoods/resid`, { params: this.parseParameters(parameters) });
  }

  fetchDistrictsSeasonal(parameters) {
    return this.http.get(`${ApiService.BASE_URL}/thefts/districts/seasonal`, { params: this.parseParameters(parameters) });
  }

  fetchNeighborhoodsSeasonal(parameters) {
    return this.http.get(`${ApiService.BASE_URL}/thefts/neighborhoods/seasonal`, { params: this.parseParameters(parameters) });
  }

  parseParameters(parameters: any = {}): HttpParams {
    let httpParams = new HttpParams();
    Object.keys(parameters).forEach(key => {
      const value = parameters[key];
      if (value instanceof Date) {
      httpParams = httpParams.set(key, this.dateService.format(value, 'YYYY-MM-DD'));
      } else {
        httpParams = httpParams.set(key, value);
      }
    });
    return httpParams;
  }

}
