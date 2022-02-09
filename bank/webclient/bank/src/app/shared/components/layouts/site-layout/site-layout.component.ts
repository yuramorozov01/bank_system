import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../../services/auth/auth.service';
import { MaterializeService } from '../../../services/utils/materialize.service';

@Component({
	selector: 'app-site-layout',
	templateUrl: './site-layout.component.html',
	styleUrls: ['./site-layout.component.css']
})
export class SiteLayoutComponent implements OnInit, AfterViewInit {

	@ViewChild('floating') floatingRef: ElementRef;

	links = [
		{
			url: '/client',
			name: 'All clients',
		},
        {
			url: '/bank_account',
			name: 'Bank accounts',
		},
	];

	constructor(private auth: AuthService,
							private router: Router) { }

	ngOnInit(): void {
	}

	ngAfterViewInit(): void {
		MaterializeService.initializeFloatingButton(this.floatingRef);
	}

	logout(event: Event) {
		event.preventDefault();
		this.auth.logout();
		this.router.navigate(['/']);
	}

}
