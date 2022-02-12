import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { FormGroup, FormControl, Validators, ValidatorFn } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { Observable } from 'rxjs';

import { switchMap } from 'rxjs/operators';
import { of } from 'rxjs';

import * as moment from 'moment';

import { IClientList } from '../../shared/interfaces/client.interfaces';
import { IDepositContract, IDepositTypeList } from '../../shared/interfaces/deposit-contract.interfaces';

import { ClientService } from '../../shared/services/client/client.service';
import { DepositContractService } from '../../shared/services/deposit-contract/deposit-contract.service';
import { DepositTypeService } from '../../shared/services/deposit-contract/deposit-type/deposit-type.service';
import { MaterializeService } from '../../shared/services/utils/materialize.service';

@Component({
    selector: 'app-deposit-contract-page',
    templateUrl: './deposit-contract-page.component.html',
    styleUrls: ['./deposit-contract-page.component.css']
})
export class DepositContractPageComponent implements OnInit {
	@ViewChild('input') inputRef: ElementRef;

	form: FormGroup;
	isNew = true;
	depositContract: IDepositContract;
    depositTypes$: Observable<IDepositTypeList[]>;
    clients$: Observable<IClientList[]>;

	constructor(private router: Router,
				private route: ActivatedRoute,
				private depositContractService: DepositContractService,
                private datePipe: DatePipe,
                private clientService: ClientService,
                private depositTypeService: DepositTypeService) { }

	ngOnInit(): void {
        let curDate = new Date();
        this.form = new FormGroup({
            deposit_type: new FormControl(null, [Validators.required,]),
            starts_at: new FormControl(this.datePipe.transform(curDate,'yyyy-MM-dd'), [Validators.required, this.dateValidator]),
            ends_at: new FormControl(this.datePipe.transform(curDate,'yyyy-MM-dd'), [Validators.required, this.dateValidator]),
            deposit_amount: new FormControl(null, [Validators.required, Validators.min(0), Validators.max(999999999999999999.99)]),
            client: new FormControl(null, Validators.required),
		});

		this.form.disable();

		this.route.params
			.pipe(
				switchMap(
					(params: Params) => {
						if (params['id']) {
							this.isNew = false;
							return this.depositContractService.getById(params['id']);
						} else {
                            this.fetchNestedObjects();
                        }
						return of(null);
					}
				)
			)
			.subscribe(
				(depositContract: IDepositContract) => {
					if (depositContract) {
						this.depositContract = depositContract;
                        this.fetchNestedObjects();
						this.form.patchValue(depositContract);
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
			obs$ = this.depositContractService.create(this.form);
		} else {
            const decision = window.confirm('Are you sure you want to revoke this deposit contract?');
            if (decision) {
                obs$ = this.depositContractService.revoke(this.depositContract.id);
            }
		}
		obs$.subscribe(
			(depositContract: IDepositContract) => {
				this.depositContract = depositContract;
                this.fetchNestedObjects();
                this.form.patchValue(depositContract);
				MaterializeService.updateTextInputs();
				MaterializeService.toast({'Success': 'Deposit contract has been saved successfully'});
				this.form.enable();
			},
			error => {
				MaterializeService.toast(error.error);
				this.form.enable();
			}
		);
	}

    dateValidator(control: FormControl): { [s: string]: boolean } {
        if (control.value) {
            const date = moment(control.value);
            const today = moment();
            if (date.isBefore(today)) {
                return {'invalidDate': true}
            }
        }
        return null;
    }

    fetchNestedObjects() {
        this.depositTypes$ = this.depositTypeService.fetch();
        this.depositTypes$.subscribe(
            (depositTypes: IDepositTypeList[]) => {
            },
            error => {
                MaterializeService.toast(error.error);
            }
        )
        this.clients$ = this.clientService.fetch();
        this.clients$.subscribe(
            (clients: IClientList[]) => {
            },
            error => {
                MaterializeService.toast(error.error);
            }
        )
    }
}
