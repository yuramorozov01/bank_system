import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AuthLayoutComponent } from './shared/components/layouts/auth-layout/auth-layout.component';
import { SiteLayoutComponent } from './shared/components/layouts/site-layout/site-layout.component';

import { LoginPageComponent } from './login-page/login-page.component';
import { RegisterPageComponent } from './register-page/register-page.component';
import { ClientsPageComponent } from "./clients-page/clients-page.component";
import { ClientPageComponent } from "./clients-page/client-page/client-page.component";
import { BankAccountsPageComponent } from './bank-accounts-page/bank-accounts-page.component';
import { DepositsPageComponent } from './deposits-page/deposits-page.component'
import { DepositPageComponent } from './deposits-page/deposit-page/deposit-page.component'
import { DepositTypesPageComponent } from './deposits-page/deposit-types-page/deposit-types-page.component'
import { DepositTypePageComponent } from './deposits-page/deposit-types-page/deposit-type-page/deposit-type-page.component'

import { AuthGuard } from './shared/services/auth/auth.guard';


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
                path: 'deposit',
                component: DepositsPageComponent,
            },
            {
                path: 'deposit/new',
                component: DepositPageComponent,
            },
            {
                path: 'deposit/:id',
                component: DepositPageComponent,
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
