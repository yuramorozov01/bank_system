import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { FormGroup, FormControl, Validators, ValidatorFn } from '@angular/forms';

import { switchMap } from 'rxjs/operators';
import { of } from 'rxjs';

import { IDepositType } from '../../../shared/interfaces/deposit.interfaces';

import { DepositTypeService } from '../../../shared/services/deposit/deposit-type/deposit-type.service';
import { MaterializeService } from '../../../shared/services/utils/materialize.service';

@Component({
  selector: 'app-deposit-type-page',
  templateUrl: './deposit-type-page.component.html',
  styleUrls: ['./deposit-type-page.component.css']
})
export class DepositTypePageComponent implements OnInit {
	@ViewChild('input') inputRef: ElementRef;

	form: FormGroup;
	isNew = true;
	depositType: IDepositType;

    currencyValues = {
        'BYN': 'BYN',
        'USD': 'USD',
        'EUR': 'EUR',
        'RUB': 'RUB',
    };

	constructor(private router: Router,
				private route: ActivatedRoute,
				private depositTypeService: DepositTypeService) { }

	ngOnInit(): void {
        this.form = new FormGroup({
            name: new FormControl(null, [Validators.required,]),
            percent: new FormControl(null, [Validators.required, Validators.min(0)]),
            deposit_term: new FormControl(null, [Validators.required, Validators.min(1)]),
            currency: new FormControl(null, [Validators.required,]),
            min_downpayment: new FormControl(null, [Validators.required, Validators.min(0), Validators.max(999999999999999999.99)]),
            max_downpayment: new FormControl(null, [Validators.min(0), Validators.max(999999999999999999.99)]),
            is_revocable: new FormControl(false, [Validators.required,]),
		});

		this.form.disable();

		this.route.params
			.pipe(
				switchMap(
					(params: Params) => {
						if (params['id']) {
							this.isNew = false;
							return this.depositTypeService.getById(params['id']);
						}
						return of(null);
					}
				)
			)
			.subscribe(
				(depositType: IDepositType) => {
					if (depositType) {
						this.depositType = depositType;
						this.form.patchValue(depositType);
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
			obs$ = this.depositTypeService.create(this.form);
		} else {
			obs$ = this.depositTypeService.update(this.depositType.id, this.form);
		}
		obs$.subscribe(
			(depositType: IDepositType) => {
				this.depositType = depositType;
                this.form.patchValue(depositType);
				MaterializeService.updateTextInputs();
				MaterializeService.toast({'Success': 'Deposit type has been saved successfully'});
				this.form.enable();
			},
			error => {
				MaterializeService.toast(error.error);
				this.form.enable();
			}
		);
	}

	deleteDepositType() {
		const decision = window.confirm('Are you sure you want to delete this deposit type?');
		if (decision) {
			this.depositTypeService.delete(this.depositType.id)
				.subscribe(
					response => MaterializeService.toast({'Success': 'Deposit type has been deleted successfully'}),
					error => MaterializeService.toast(error.error),
					() => this.router.navigate(['/deposit_type'])
				);
		}
	}
}
