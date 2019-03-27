import { Routes, RouterModule } from '@angular/router';

import { LoginRedirect } from './services/login-redirect.service';
import { EnsureAuthenticated } from './services/ensure-authenticated.service';

import { NavbarLayoutComponent
} from './components/_layout/navbar-layout/navbar-layout.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { StatusComponent } from './components/status/status.component';
import { PropertyComponent } from './components/property/property.component';
import { TenantbillEditComponent
} from './components/tenantbill-edit/tenantbill-edit.component';
import { PropertyAddComponent
} from './components/property-add/property-add.component';
import { PropertyEditComponent
} from './components/property-edit/property-edit.component';
import { LocationAddComponent
} from './components/location-add/location-add.component';
import { LocationEditComponent
} from './components/location-edit/location-edit.component';

const appRoutes: Routes = [
  {
    path: 'login',
    component: LoginComponent,
    canActivate: [LoginRedirect]
  },
  {
    path: 'register',
    component: RegisterComponent,
    canActivate: [LoginRedirect]
  },
  {
    path: '',
    component: NavbarLayoutComponent,
    children: [
      {
        path: 'dashboard',
        component: DashboardComponent
      },
      {
        path: 'property',
        component: PropertyComponent
      },
      {
        path: 'tenantbill/edit',
        component: TenantbillEditComponent
      },
      {
        path: 'property/add',
        component: PropertyAddComponent
      },
      {
        path: 'property/edit',
        component: PropertyEditComponent
      },
      {
        path: 'location/add',
        component: LocationAddComponent
      },
      {
        path: 'location/edit',
        component: LocationEditComponent
      }
    ]// ,
    // canActivate: [EnsureAuthenticated]
  },
  {
    path: 'status',
    component: StatusComponent,
    canActivate: [EnsureAuthenticated]
  }
];

export const routing = RouterModule.forRoot(appRoutes);
