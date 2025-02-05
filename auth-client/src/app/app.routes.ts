import { Routes } from '@angular/router';
import { AuthFormComponent } from './pages/auth-form/auth-form.component';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () =>
      import('./components/layout/layout.component').then(
        (c) => c.LayoutComponent
      ),
    canActivate: [],
    children: [],
  },
  {
    path: 'auth',
    component: AuthFormComponent,
    // loadComponent: () => import("./pages/auth-form/auth-form.component").then(c => c.AuthFormComponent),
  },
];
