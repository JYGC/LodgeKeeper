import { Routes, RouterModule } from '@angular/router';

import { LoginRedirect } from './services/login-redirect.service';
import { EnsureAuthenticated } from './services/ensure-authenticated.service';

import { NavbarLayoutComponent
} from './components/_layout/navbar-layout/navbar-layout.component';
import { LoginComponent } from './components/login/login.component';
import { RegisterComponent } from './components/register/register.component';
import { TenancyListAllComponent 
} from './components/tenancy-list-all/tenancy-list-all.component';
import { TenancyAddComponent
} from './components/tenancy-add/tenancy-add.component';
import { StatusComponent } from './components/status/status.component';
import { TenantbillEditComponent
} from './components/tenantbill-edit/tenantbill-edit.component';

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
    canActivate: [EnsureAuthenticated],
    children: [
      {
        path: 'tenancy/list-all',
        component: TenancyListAllComponent
      },
      {
        path: 'tenancy/add',
        component: TenancyAddComponent
      },
      {
        path: 'tenantbill/edit',
        component: TenantbillEditComponent
      }
    ]
  },
  {
    path: 'status',
    component: StatusComponent,
    canActivate: [EnsureAuthenticated]
  }
];

export const routing = RouterModule.forRoot(appRoutes);
