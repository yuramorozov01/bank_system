import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { AuthLayoutComponent } from './shared/components/layouts/auth-layout/auth-layout.component';
import { SiteLayoutComponent } from './shared/components/layouts/site-layout/site-layout.component';

import { LoginPageComponent } from './login-page/login-page.component';
import { RegisterPageComponent } from './register-page/register-page.component';
import { ClientsPageComponent } from "./clients-page/clients-page.component";
import { ClientPageComponent } from "./clients-page/client-page/client-page.component";

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
				path: 'client/:id',
				component: ClientPageComponent
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
