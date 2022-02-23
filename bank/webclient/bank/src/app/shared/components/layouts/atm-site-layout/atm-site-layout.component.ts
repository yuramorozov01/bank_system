import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { AtmAuthService } from '../../../services/auth/atm-auth/atm-auth.service';

@Component({
  selector: 'app-atm-site-layout',
  templateUrl: './atm-site-layout.component.html',
  styleUrls: ['./atm-site-layout.component.css']
})
export class AtmSiteLayoutComponent implements OnInit {

	links = [
        {
            url: '/login',
            name: 'Bank',
        },
        {
            url: '/atm/balance',
            name: 'Balance',
        },
        {
            url: '/atm/withdraw',
            name: 'Withdraw money',
        },
	];

	constructor(private atmAuth: AtmAuthService,
                private router: Router) { }

	ngOnInit(): void {
	}

	logout(event: Event) {
		event.preventDefault();
		this.atmAuth.logout();
		this.router.navigate(['/atm']);
	}

}
