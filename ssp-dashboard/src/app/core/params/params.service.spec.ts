import { TestBed, inject } from '@angular/core/testing';

import { \core\params\paramsService } from './\core\params\params.service';

describe('\core\params\paramsService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [\core\params\paramsService]
    });
  });

  it('should be created', inject([\core\params\paramsService], (service: \core\params\paramsService) => {
    expect(service).toBeTruthy();
  }));
});
