import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { AuthService } from './services/auth.service';
import { RegisterComponent } from './components/register/register.component';
import { StatusComponent } from './components/status/status.component';
import { LoginRedirect } from './services/login-redirect.service';
import { EnsureAuthenticated } from './services/ensure-authenticated.service';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { TenantbillEditComponent
} from './components/tenantbill-edit/tenantbill-edit.component';
import { PropertyComponent } from './components/property/property.component';
import { PropertyAddComponent
} from './components/property-add/property-add.component';
import { PropertyEditComponent
} from './components/property-edit/property-edit.component';
import { AreaAddComponent } from './components/area-add/area-add.component';
import { AreaEditComponent } from './components/area-edit/area-edit.component';
import { ExtrachargeComponent
} from './components/extracharge/extracharge.component';
import { ExtrachargeAddComponent
} from './components/extracharge-add/extracharge-add.component';
import { ExtrachargeEditComponent
} from './components/extracharge-edit/extracharge-edit.component';
import { TenancyComponent } from './components/tenancy/tenancy.component';
import { TenancyAddComponent
} from './components/tenancy-add/tenancy-add.component';
import { TenancyEditComponent
} from './components/tenancy-edit/tenancy-edit.component';
import { TenantComponent } from './components/tenant/tenant.component';
import { TenantAddComponent
} from './components/tenant-add/tenant-add.component';
import { TenantEditComponent
} from './components/tenant-edit/tenant-edit.component';
import { NavbarLayoutComponent
} from './components/_layout/navbar-layout/navbar-layout.component';
import { NavbarHeaderComponent
} from './components/_layout/navbar-header/navbar-header.component';

import { routing } from './app.routing';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    StatusComponent,
    DashboardComponent,
    TenantbillEditComponent,
    PropertyComponent,
    PropertyAddComponent,
    PropertyEditComponent,
    AreaAddComponent,
    AreaEditComponent,
    ExtrachargeComponent,
    ExtrachargeAddComponent,
    ExtrachargeEditComponent,
    TenancyComponent,
    TenancyAddComponent,
    TenancyEditComponent,
    TenantComponent,
    TenantAddComponent,
    TenantEditComponent,
    NavbarLayoutComponent,
    NavbarHeaderComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    routing
  ],
  providers: [
    AuthService,
    EnsureAuthenticated,
    LoginRedirect
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
