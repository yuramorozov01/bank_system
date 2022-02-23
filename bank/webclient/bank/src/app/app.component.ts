import { Component, OnInit } from '@angular/core';

import { AuthService } from './shared/services/auth/auth.service';
import { AtmAuthService } from './shared/services/auth/atm-auth/atm-auth.service';

@Component({
	selector: 'app-root',
	templateUrl: './app.component.html',
})
export class AppComponent implements OnInit {
	constructor(private auth: AuthService,
                private atmAuth: AtmAuthService) {

	}

	ngOnInit() {
		const potentialToken = localStorage.getItem('auth-token');
		if (potentialToken !== null) {
			this.auth.setAccessToken(potentialToken);
		}

        const potentialTokenAtm = localStorage.getItem('atm-auth-token');
		if (potentialTokenAtm !== null) {
			this.atmAuth.setAccessToken(potentialTokenAtm);
		}
	}
}
