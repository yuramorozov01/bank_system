import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { FormGroup, FormControl, Validators, ValidatorFn } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { Observable } from 'rxjs';

import { switchMap } from 'rxjs/operators';
import { of } from 'rxjs';

import * as moment from 'moment';

import { IClientList } from '../../shared/interfaces/client.interfaces';
import { ICreditContract, ICreditTypeList } from '../../shared/interfaces/credit-contract.interfaces';

import { ClientService } from '../../shared/services/client/client.service';
import { CreditContractService } from '../../shared/services/credit-contract/credit-contract.service';
import { CreditTypeService } from '../../shared/services/credit-contract/credit-type/credit-type.service';
import { MaterializeService } from '../../shared/services/utils/materialize.service';

@Component({
    selector: 'app-credit-contract-page',
    templateUrl: './credit-contract-page.component.html',
    styleUrls: ['./credit-contract-page.component.css']
})
export class CreditContractPageComponent implements OnInit {
	@ViewChild('input') inputRef: ElementRef;

	form: FormGroup;
	isNew = true;
	creditContract: ICreditContract;
    creditTypes$: Observable<ICreditTypeList[]>;
    clients$: Observable<IClientList[]>;

	constructor(private router: Router,
				private route: ActivatedRoute,
				private creditContractService: CreditContractService,
                private datePipe: DatePipe,
                private clientService: ClientService,
                private creditTypeService: CreditTypeService) { }

	ngOnInit(): void {
        let curDate = new Date();
        this.form = new FormGroup({
            credit_type: new FormControl(null, [Validators.required,]),
            starts_at: new FormControl(this.datePipe.transform(curDate,'yyyy-MM-dd'), [Validators.required, this.dateValidator]),
            ends_at: new FormControl(this.datePipe.transform(curDate,'yyyy-MM-dd'), [Validators.required, this.dateValidator]),
            credit_amount: new FormControl(null, [Validators.required, Validators.min(0), Validators.max(999999999999999999.99)]),
            client: new FormControl(null, Validators.required),
            pin: new FormControl(null, [Validators.required, Validators.pattern('^[0-9]{3}$')]),
		});

		this.form.disable();

		this.route.params
			.pipe(
				switchMap(
					(params: Params) => {
						if (params['id']) {
							this.isNew = false;
							return this.creditContractService.getById(params['id']);
						} else {
                            this.fetchNestedObjects();
                        }
						return of(null);
					}
				)
			)
			.subscribe(
				(creditContract: ICreditContract) => {
					if (creditContract) {
						this.creditContract = creditContract;
                        this.fetchNestedObjects();
						this.form.patchValue(creditContract);
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
			obs$ = this.creditContractService.create(this.form);
		} else {
            const decision = window.confirm('Are you sure you want to pay off this credit contract?');
            if (decision) {
                obs$ = this.creditContractService.payOff(this.creditContract.id);
            }
		}
		obs$.subscribe(
			(creditContract: ICreditContract) => {
                this.form.enable();
                this.isNew = false;
                MaterializeService.toast({'Success': 'Credit contract has been saved successfully'});
                this.router.navigate(['/credit_contract', creditContract.id]);
			},
			error => {
				MaterializeService.toast(error.error);
				this.form.enable();
			}
		);
	}

    dateValidator(control: FormControl): { [s: string]: boolean } {
        if (control.value) {
            const date = moment(control.value).toDate().getDate();
            const today = moment().toDate().getDate();
            if (date < today) {
                return {'invalidDate': true}
            }
        }
        return null;
    }

    fetchNestedObjects() {
        this.creditTypes$ = this.creditTypeService.fetch();
        this.creditTypes$.subscribe(
            (creditTypes: ICreditTypeList[]) => {
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
