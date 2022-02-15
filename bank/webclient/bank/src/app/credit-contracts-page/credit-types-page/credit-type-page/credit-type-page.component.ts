import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { FormGroup, FormControl, Validators, ValidatorFn } from '@angular/forms';

import { switchMap } from 'rxjs/operators';
import { of } from 'rxjs';

import { ICreditType } from '../../../shared/interfaces/credit-contract.interfaces';

import { CreditTypeService } from '../../../shared/services/credit-contract/credit-type/credit-type.service';
import { MaterializeService } from '../../../shared/services/utils/materialize.service';

@Component({
  selector: 'app-credit-type-page',
  templateUrl: './credit-type-page.component.html',
  styleUrls: ['./credit-type-page.component.css']
})
export class CreditTypePageComponent implements OnInit {
	@ViewChild('input') inputRef: ElementRef;

	form: FormGroup;
	isNew = true;
	creditType: ICreditType;

    currencyValues = {
        'BYN': 'BYN',
        'USD': 'USD',
        'EUR': 'EUR',
        'RUB': 'RUB',
    };

	constructor(private router: Router,
				private route: ActivatedRoute,
				private creditTypeService: CreditTypeService) { }

	ngOnInit(): void {
        this.form = new FormGroup({
            name: new FormControl(null, [Validators.required,]),
            percent: new FormControl(null, [Validators.required, Validators.min(0)]),
            credit_term: new FormControl(null, [Validators.required, Validators.min(1)]),
            currency: new FormControl(null, [Validators.required,]),
            min_downpayment: new FormControl(null, [Validators.required, Validators.min(0), Validators.max(999999999999999999.99)]),
            max_downpayment: new FormControl(null, [Validators.min(0), Validators.max(999999999999999999.99)]),
            is_annuity_payment: new FormControl(false, [Validators.required,]),
		});

		this.form.disable();

		this.route.params
			.pipe(
				switchMap(
					(params: Params) => {
						if (params['id']) {
							this.isNew = false;
							return this.creditTypeService.getById(params['id']);
						}
						return of(null);
					}
				)
			)
			.subscribe(
				(creditType: ICreditType) => {
					if (creditType) {
						this.creditType = creditType;
						this.form.patchValue(creditType);
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

		if (this.isNew) {
			obs$ = this.creditTypeService.create(this.form);
		} else {
			obs$ = this.creditTypeService.update(this.creditType.id, this.form);
		}
		obs$.subscribe(
			(creditType: ICreditType) => {
				this.creditType = creditType;
                this.form.patchValue(creditType);
				MaterializeService.updateTextInputs();
				MaterializeService.toast({'Success': 'Credit type has been saved successfully'});
				this.form.enable();
			},
			error => {
				MaterializeService.toast(error.error);
				this.form.enable();
			}
		);
	}

	deleteCreditType() {
		const decision = window.confirm('Are you sure you want to delete this credit type?');
		if (decision) {
			this.creditTypeService.delete(this.creditType.id)
				.subscribe(
					response => MaterializeService.toast({'Success': 'Credit type has been deleted successfully'}),
					error => MaterializeService.toast(error.error),
					() => this.router.navigate(['/credit_type'])
				);
		}
	}
}
