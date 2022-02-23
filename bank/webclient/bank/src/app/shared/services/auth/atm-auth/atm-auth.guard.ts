import { CanActivate, CanActivateChild, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable, of } from 'rxjs';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';

import { AtmAuthService } from './atm-auth.service';

@Injectable({
	providedIn: 'root'
})
export class AtmAuthGuard implements CanActivate, CanActivateChild {
	constructor(private atmAuth: AtmAuthService,
				private router: Router) {

	}

	canActivate(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {
		if (this.atmAuth.isAuthenticated()) {
			return of(true);
		} else {
			this.router.navigate(['/'], {
				queryParams: {
					accessDenied: true,
				},
			});
			return of(false);
		}
	}

	canActivateChild(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean> {
		return this.canActivate(route, state);
	}
}
