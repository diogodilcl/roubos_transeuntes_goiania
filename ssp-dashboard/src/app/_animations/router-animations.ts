import { animate, group, query, stagger, style, transition, trigger } from '@angular/animations';

export const ROUTER_ANIMATION = trigger('routerAnimations', [
  transition(':enter, initial => *', []),
  transition('* => *', [
    style({position: 'relative'}),
    query(':enter, :leave', style({position: 'absolute', top: 0, left: 0, right: 0})),
    query(':enter mat-card', [
      style({opacity: 0, transform: 'translateY(100%)'})
    ]),
    group([
      query(':leave mat-card', stagger('200ms', [
        animate('600ms cubic-bezier(.35,0,.25,1)', style({transform: 'translateY(-100%)', opacity: 0}))
      ])),
      query(':enter mat-card', stagger('200ms', [
        animate('600ms cubic-bezier(.35,0,.25,1)', style({opacity: 1, transform: 'translateY(0%)'})),
      ])),
    ]),
  ])
]);
