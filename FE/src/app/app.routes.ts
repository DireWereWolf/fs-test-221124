import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./pages/home-page/home-page.component').then((m) => m.HomePageComponent)
  },{
    path: 'user',
    loadComponent: () =>
      import('./pages/user-page/user-page.component').then((m) => m.UserPageComponent)
  },{
    path: 'user/:id',
    loadComponent: () =>
      import('./pages/user-page/user-page.component').then((m) => m.UserPageComponent)
  },
  { path: '**', redirectTo: '', pathMatch: 'full' }
];
