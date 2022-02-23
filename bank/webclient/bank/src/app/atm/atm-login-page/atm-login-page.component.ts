import { Component, OnInit, OnDestroy } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { Subscription } from 'rxjs';

import { AtmAuthService } from '../../shared/services/auth/atm-auth/atm-auth.service';
import { MaterializeService } from '../../shared/services/utils/materialize.service';

@Component({
  selector: 'app-atm-login-page',
  templateUrl: './atm-login-page.component.html',
  styleUrls: ['./atm-login-page.component.css']
})
export class AtmLoginPageComponent implements OnInit {
	form: FormGroup;

	aSub: Subscription;

	constructor(private atmAuth: AtmAuthService,
				private router: Router,
				private route: ActivatedRoute) { }

	ngOnInit(): void {
        if (this.atmAuth.isAuthenticated()) {
            this.router.navigate(['/atm/balance']);
        }

		this.form = new FormGroup({
			number: new FormControl(null, [Validators.required, Validators.pattern('^[0-9]{16}$')]),
			pin: new FormControl(null, [Validators.required, Validators.pattern('^[0-9]{3}$')]),
		});
	}

	ngOnDestroy(): void {
		if (this.aSub) {
			this.aSub.unsubscribe();
		}
	}

	onSubmit() {
		this.form.disable();
		this.aSub = this.atmAuth.auth(this.form).subscribe(
			(tokens: any) => {
				this.router.navigate(['/atm/balance']);
			},
			error => {
				MaterializeService.toast(error.error);
				this.form.enable();
			}
		);
	}

}
