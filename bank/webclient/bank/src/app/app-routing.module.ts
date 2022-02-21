import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AuthLayoutComponent } from './shared/components/layouts/auth-layout/auth-layout.component';
import { SiteLayoutComponent } from './shared/components/layouts/site-layout/site-layout.component';

import { LoginPageComponent } from './login-page/login-page.component';
import { RegisterPageComponent } from './register-page/register-page.component';
import { ClientsPageComponent } from "./clients-page/clients-page.component";
import { ClientPageComponent } from "./clients-page/client-page/client-page.component";
import { BankAccountsPageComponent } from './bank-accounts-page/bank-accounts-page.component';
import { DepositContractsPageComponent } from './deposit-contracts-page/deposit-contracts-page.component';
import { DepositContractPageComponent } from './deposit-contracts-page/deposit-contract-page/deposit-contract-page.component';
import { DepositTypesPageComponent } from './deposit-contracts-page/deposit-types-page/deposit-types-page.component';
import { DepositTypePageComponent } from './deposit-contracts-page/deposit-types-page/deposit-type-page/deposit-type-page.component';
import { ManagerPanelPageComponent } from './manager-panel-page/manager-panel-page.component';

import { AuthGuard } from './shared/services/auth/auth.guard';
import { BankAccountPageComponent } from './bank-accounts-page/bank-account-page/bank-account-page.component';
import { CreditContractPageComponent } from './credit-contracts-page/credit-contract-page/credit-contract-page.component';
import { CreditContractsPageComponent } from './credit-contracts-page/credit-contracts-page.component';
import { CreditTypesPageComponent } from './credit-contracts-page/credit-types-page/credit-types-page.component';
import { CreditTypePageComponent } from './credit-contracts-page/credit-types-page/credit-type-page/credit-type-page.component';


const routes: Routes = [
	{
		path: '',
		component: AuthLayoutComponent,
		children: [
			{
				path: '',
				redirectTo: '/login',
				pathMatch: 'full',
			},
			{
				path: 'login',
				component: LoginPageComponent,
			},
			{
				path: 'register',
				component: RegisterPageComponent,
			},
		],
	},
	{
		path: '',
		component: SiteLayoutComponent,
		canActivate: [AuthGuard],
		children: [
			{
				path: '',
				redirectTo: '/client',
				pathMatch: 'full',
			},
			{
				path: 'client',
				component: ClientsPageComponent
			},
            {
				path: 'client/new',
				component: ClientPageComponent
			},
			{
				path: 'client/:id',
				component: ClientPageComponent
			},
            {
                path: 'bank_account',
                component: BankAccountsPageComponent,
            },
            {
                path: 'bank_account/:id',
                component: BankAccountPageComponent,
            },
            {
                path: 'deposit_contract',
                component: DepositContractsPageComponent,
            },
            {
                path: 'deposit_contract/new',
                component: DepositContractPageComponent,
            },
            {
                path: 'deposit_contract/:id',
                component: DepositContractPageComponent,
            },
            {
                path: 'deposit_type',
                component: DepositTypesPageComponent,
            },
            {
                path: 'deposit_type/new',
                component: DepositTypePageComponent,
            },
            {
                path: 'deposit_type/:id',
                component: DepositTypePageComponent,
            },
            {
                path: 'credit_contract',
                component: CreditContractsPageComponent,
            },
            {
                path: 'credit_contract/new',
                component: CreditContractPageComponent,
            },
            {
                path: 'credit_contract/:id',
                component: CreditContractPageComponent,
            },
            {
                path: 'credit_type',
                component: CreditTypesPageComponent,
            },
            {
                path: 'credit_type/new',
                component: CreditTypePageComponent,
            },
            {
                path: 'credit_type/:id',
                component: CreditTypePageComponent,
            },
            {
                path: 'manager',
                component: ManagerPanelPageComponent,
            },
		],
	},
];

@NgModule({
	imports: [
		RouterModule.forRoot(routes),
	],
	exports: [
		RouterModule,
	],
})
export class AppRoutingModule {
}
