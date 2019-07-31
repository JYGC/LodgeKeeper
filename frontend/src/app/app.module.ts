import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { UiSwitchModule } from 'ngx-toggle-switch';
import { ArchwizardModule } from 'angular-archwizard';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { DlDateTimeDateModule, DlDateTimePickerModule
} from 'angular-bootstrap-datetimepicker';

import { AppComponent } from './app.component';
import { LoginComponent } from './components/login/login.component';
import { AuthService } from './services/auth.service';
import { RegisterComponent } from './components/register/register.component';
import { StatusComponent } from './components/status/status.component';
import { LoginRedirect } from './services/login-redirect.service';
import { EnsureAuthenticated } from './services/ensure-authenticated.service';
import { TenancyListAllComponent
} from './components/tenancy-list-all/tenancy-list-all.component';
import { TenantbillEditComponent
} from './components/tenantbill-edit/tenantbill-edit.component';
import { TenancyAddComponent
} from './components/tenancy-add/tenancy-add.component';
import { TenantNamesComponent
} from './components/tenancy-add-wizard/tenant-names/tenant-names.component';
import { StartEndDateComponent
} from './components/tenancy-add-wizard/start-end-date/start-end-date.component';
import { RentPaymentComponent
} from './components/tenancy-add-wizard/rent-payment/rent-payment.component';
import { PropertyDetailsComponent
} from './components/tenancy-add-wizard/property-details/property-details.component';
import { NotificationSchedulingComponent
} from './components/tenancy-add-wizard/notification-scheduling/notification-scheduling.component';
import { ConfirmationComponent
} from './components/tenancy-add-wizard/confirmation/confirmation.component';
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
import { TenancyAddService } from './services/tenancy-add.service';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    StatusComponent,
    TenancyListAllComponent,
    TenantbillEditComponent,
    TenancyAddComponent,
    TenancyEditComponent,
    TenantComponent,
    TenantAddComponent,
    TenantEditComponent,
    NavbarLayoutComponent,
    NavbarHeaderComponent,
    TenantNamesComponent,
    StartEndDateComponent,
    RentPaymentComponent,
    PropertyDetailsComponent,
    NotificationSchedulingComponent,
    ConfirmationComponent
  ],
  imports: [
    BrowserModule,
    UiSwitchModule,
    HttpClientModule,
    FormsModule,
    ArchwizardModule,
    DlDateTimeDateModule,
    DlDateTimePickerModule,
    NgbModule,
    routing
  ],
  providers: [
    AuthService,
    EnsureAuthenticated,
    LoginRedirect,
    TenancyAddService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
