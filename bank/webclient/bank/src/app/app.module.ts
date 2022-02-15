import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { DatePipe } from '@angular/common';
import { environment } from '../environments/environment';

import { AppComponent } from './app.component';
import { LoginPageComponent } from './login-page/login-page.component';
import { AppRoutingModule } from './app-routing.module';
import { AuthLayoutComponent } from './shared/components/layouts/auth-layout/auth-layout.component';
import { SiteLayoutComponent } from './shared/components/layouts/site-layout/site-layout.component';
import { RegisterPageComponent } from './register-page/register-page.component';
import { TokenInterceptor } from './shared/services/auth/token.interceptor';
import { LoaderComponent } from './shared/components/loader/loader.component';
import { ClientsPageComponent } from './clients-page/clients-page.component';
import { ClientPageComponent } from './clients-page/client-page/client-page.component';
import { DepositContractsPageComponent } from './deposit-contracts-page/deposit-contracts-page.component';
import { BankAccountsPageComponent } from './bank-accounts-page/bank-accounts-page.component';
import { ManagerPanelPageComponent } from './manager-panel-page/manager-panel-page.component';
import { DepositContractPageComponent } from './deposit-contracts-page/deposit-contract-page/deposit-contract-page.component';
import { DepositTypesPageComponent } from './deposit-contracts-page/deposit-types-page/deposit-types-page.component';
import { DepositTypePageComponent } from './deposit-contracts-page/deposit-types-page/deposit-type-page/deposit-type-page.component';
import { TopUpBankAccountPageComponent } from './bank-accounts-page/top-up-bank-account-page/top-up-bank-account-page.component';
import { CreditContractsPageComponent } from './credit-contracts-page/credit-contracts-page.component';
import { CreditContractPageComponent } from './credit-contracts-page/credit-contract-page/credit-contract-page.component';
import { CreditTypesPageComponent } from './credit-contracts-page/credit-types-page/credit-types-page.component';
import { CreditTypePageComponent } from './credit-contracts-page/credit-types-page/credit-type-page/credit-type-page.component';

@NgModule({
    declarations: [
        AppComponent,
        LoginPageComponent,
        AuthLayoutComponent,
        SiteLayoutComponent,
        RegisterPageComponent,
        LoaderComponent,
        ClientsPageComponent,
        ClientPageComponent,
        DepositContractsPageComponent,
        BankAccountsPageComponent,
        ManagerPanelPageComponent,
        DepositContractPageComponent,
        DepositTypesPageComponent,
        DepositTypePageComponent,
        TopUpBankAccountPageComponent,
        CreditContractsPageComponent,
        CreditContractPageComponent,
        CreditTypesPageComponent,
        CreditTypePageComponent,
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        FormsModule,
        ReactiveFormsModule,
        HttpClientModule,
    ],
    providers: [
        {
            provide: HTTP_INTERCEPTORS,
            multi: true,
            useClass: TokenInterceptor,
        },
        DatePipe,
    ],
    bootstrap: [AppComponent]
})
export class AppModule { }
