import { TestBed } from '@angular/core/testing';

import { TenancyAddService } from './tenancy-add.service';

describe('TenancyAddService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: TenancyAddService = TestBed.get(TenancyAddService);
    expect(service).toBeTruthy();
  });
});
