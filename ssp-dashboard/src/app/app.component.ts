import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import { ROUTER_ANIMATION } from './_animations/router-animations';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  animations: [ROUTER_ANIMATION]
})
export class AppComponent {

  links = [
    { path: '/', icon: 'home', label: 'Home'},
    { path: '/bairros', icon: 'info', label: 'Bairros'},
    { path: '/regioes', icon: 'info', label: 'Regiões'},
    { path: '/about', icon: 'info', label: 'Items'}
  ];

  prepareRouterState(router: RouterOutlet) {
    return router.activatedRouteData['animation'] || 'initial';
  }

}
