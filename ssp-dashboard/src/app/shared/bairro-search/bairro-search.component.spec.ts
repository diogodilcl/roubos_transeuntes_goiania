import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BairroSearchComponent } from './bairro-search.component';

describe('BairroSearchComponent', () => {
  let component: BairroSearchComponent;
  let fixture: ComponentFixture<BairroSearchComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BairroSearchComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BairroSearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
