import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { FormGroup, FormControl, Validators } from '@angular/forms';

import { switchMap } from 'rxjs/operators';

import { IBankAccount } from '../../shared/interfaces/bank-account.interfaces';

import { BankAccountService } from '../../shared/services/bank-account/bank-account.service';
import { MaterializeService } from '../../shared/services/utils/materialize.service';

@Component({
  selector: 'app-bank-account-page',
  templateUrl: './bank-account-page.component.html',
  styleUrls: ['./bank-account-page.component.css']
})
export class BankAccountPageComponent implements OnInit {
	@ViewChild('input') inputRef: ElementRef;

	form: FormGroup;
	bankAccount: IBankAccount;

	constructor(private router: Router,
				private route: ActivatedRoute,
				private bankAccountService: BankAccountService) { }

	ngOnInit(): void {
        this.form = new FormGroup({
            amount: new FormControl(null, [Validators.required, Validators.min(0)]),
		});

		this.form.disable();

		this.route.params
			.pipe(
				switchMap(
					(params: Params) => {
                        return this.bankAccountService.getById(params['id']);
					}
				)
			)
			.subscribe(
				(bankAccount: IBankAccount) => {
					if (bankAccount) {
						this.bankAccount = bankAccount;
						MaterializeService.updateTextInputs();
					}
					this.form.enable();
				},
                error => MaterializeService.toast(error.error),
			);
	}

	triggerClick() {
		this.inputRef.nativeElement.click();
	}

	onSubmit() {
		let obs$;
		this.form.disable();
        obs$ = this.bankAccountService.topUp(this.bankAccount.id, this.form);
		obs$.subscribe(
			(bankAccount: IBankAccount) => {
				this.bankAccount = bankAccount;
				MaterializeService.toast({'Success': 'Balance has been topped up!'});
				this.form.enable();
			},
			error => {
				MaterializeService.toast(error.error);
				this.form.enable();
			}
		);
	}
}
