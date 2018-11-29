import { BairroSearchModule } from './bairro-search.module';

describe('BairroSearchModule', () => {
  let bairroSearchModule: BairroSearchModule;

  beforeEach(() => {
    bairroSearchModule = new BairroSearchModule();
  });

  it('should create an instance', () => {
    expect(bairroSearchModule).toBeTruthy();
  });
});
