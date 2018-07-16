import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { HomeComponent } from './home/home.component';
import { AboutComponent } from './about/about.component';
import { BairrosComponent } from './bairros/bairros.component';
import { RegioesComponent } from './regioes/regioes.component';

const routes: Routes = [
  { path: '', component: HomeComponent, data: { animation: 'home' } },
  { path: 'bairros', component: BairrosComponent, data: { animation: 'bairros' } },
  { path: 'regioes', component: RegioesComponent, data: { animation: 'regioes' } },
  { path: 'about', component: AboutComponent, data: { animation: 'about' } },
  { path: '**', redirectTo: '', pathMatch: 'full' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: []
})
export class AppRoutingModule { }
