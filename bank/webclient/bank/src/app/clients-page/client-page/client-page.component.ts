import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { FormGroup, FormControl, Validators, ValidatorFn } from '@angular/forms';
import { DatePipe } from '@angular/common';

import { switchMap } from 'rxjs/operators';
import { of } from 'rxjs';

import * as moment from 'moment';

import { IClient } from '../../shared/interfaces/client.interfaces';

import { ClientService } from '../../shared/services/client/client.service';
import { MaterializeService } from '../../shared/services/utils/materialize.service';

@Component({
	selector: 'app-client-page',
	templateUrl: './client-page.component.html',
	styleUrls: ['./client-page.component.css']
})
export class ClientPageComponent implements OnInit {
	@ViewChild('input') inputRef: ElementRef;

	form: FormGroup;
	isNew = true;
	client: IClient;

    sexValues = {
        'Male': 'Male',
        'Female': 'Female',
        'X': 'X',
    };

    cityValues = {
        'Minsk': 'Minsk',
        'Mogilev': 'Mogilev',
        'Vitebsk': 'Vitebsk',
        'Gomel': 'Gomel',
        'Brest': 'Brest',
        'Moscow': 'Moscow',
        'Warsawa': 'Warsawa',
        'Kyiv': 'Kyiv',
        'Vilnius': 'Vilnius',
    }

    familyStatusValues = {
        'Married': 'Married',
        'Singleness': 'Singleness',
        'Divorced': 'Divorced',
        'Common-law': 'Common-law',
    }

    citizenValues = {
        'Belarus': 'Belarus',
        'Russian': 'Russian',
        'Ukraine': 'Ukraine',
        'Poland' : 'Poland',
        'Lithuania': 'Lithuania',
    }

    disabilityValues = {
        0: 'Group 0',
        1: 'Group 1',
        2: 'Group 2',
        3: 'Group 3',
    }

    passportSeriesValues = {
        'AB': 'AB',
        'BM': 'BM',
        'HB': 'HB',
        'KH': 'KH',
        'MP': 'MP',
        'MC': 'MC',
        'KB': 'KB',
        'PP': 'PP',
        'SP': 'SP',
        'DP': 'DP',
    }

	constructor(private router: Router,
				private route: ActivatedRoute,
				private clientService: ClientService,
                private datePipe: DatePipe) { }

	ngOnInit(): void {
        let curDate = new Date();
        this.form = new FormGroup({
            last_name: new FormControl(null, [Validators.required, Validators.pattern('^[a-zA-Zа-яА-Я]+[a-zA-Zа-яА-Я-]+[a-zA-Zа-яА-Я]+$')]),
            first_name: new FormControl(null, [Validators.required, Validators.pattern('^[a-zA-Zа-яА-Я]+[a-zA-Zа-яА-Я-]+[a-zA-Zа-яА-Я]+$')]),
            patronymic: new FormControl(null, [Validators.required, Validators.pattern('^[a-zA-Zа-яА-Я]+[a-zA-Zа-яА-Я-]+[a-zA-Zа-яА-Я]+$')]),

            birthday: new FormControl(this.datePipe.transform(curDate,'yyyy-MM-dd'), [Validators.required, this.dateValidator]),
            birthday_place: new FormControl(null, [Validators.required, Validators.pattern('^[a-zA-Zа-яА-Я]+[a-zA-Zа-яА-Я-]+[a-zA-Zа-яА-Я]+$')]),
            sex: new FormControl(null, Validators.required),

            passport_series: new FormControl(null, Validators.required),
            passport_number: new FormControl(null, [Validators.required, Validators.pattern('^[0-9]{7}$')]),
            passport_issued_by: new FormControl(null, Validators.required),
            passport_issued_at: new FormControl(this.datePipe.transform(curDate,'yyyy-MM-dd'), [Validators.required, this.dateValidator]),
            id_number: new FormControl(null, [Validators.required, Validators.pattern('^[0-9]{7}[аАвВсСкКеЕмМнН][0-9]{3}(PB|BA|BI)[0-9]$')]),

            city: new FormControl(null, Validators.required),
            address: new FormControl(null, Validators.required),

            home_number: new FormControl(null, [Validators.required, Validators.pattern('^[0-9]{7}$')]),
            phone_number: new FormControl(null, [Validators.required, Validators.pattern('^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$')]),

            email: new FormControl(null, Validators.email),

            job_place: new FormControl(),
            job_position: new FormControl(),

            register_city: new FormControl(null, Validators.required),
            register_address: new FormControl(null, Validators.required),

            family_status: new FormControl(null, Validators.required),
            citizen: new FormControl(null, Validators.required),
            disability: new FormControl(null, Validators.required),
            pensioner: new FormControl(false, Validators.required),
            monthly_salary: new FormControl(null),
            army: new FormControl(false, Validators.required),
		});

		this.form.disable();

		this.route.params
			.pipe(
				switchMap(
					(params: Params) => {
						if (params['id']) {
							this.isNew = false;
							return this.clientService.getById(params['id']);
						}
						return of(null);
					}
				)
			)
			.subscribe(
				(client: IClient) => {
					if (client) {
						this.client = client;
						this.form.patchValue(client);
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
			obs$ = this.clientService.create(this.form);
		} else {
			obs$ = this.clientService.update(this.client.id, this.form);
		}
		obs$.subscribe(
			(client: IClient) => {
				this.client = client;
                this.form.patchValue(client);
				MaterializeService.updateTextInputs();
				MaterializeService.toast({'Success': 'Client has been saved successfully'});
				this.form.enable();
			},
			error => {
				MaterializeService.toast(error.error);
				this.form.enable();
			}
		);
	}

	deleteClient() {
		const decision = window.confirm('Are you sure you want to delete this client?');
		if (decision) {
			this.clientService.delete(this.client.id)
				.subscribe(
					response => MaterializeService.toast({'Success': 'Client has been deleted successfully'}),
					error => MaterializeService.toast(error.error),
					() => this.router.navigate(['/client'])
				);
		}
	}

    dateValidator(control: FormControl): { [s: string]: boolean } {
        if (control.value) {
            const date = moment(control.value);
            const today = moment();
            if (date.isAfter(today)) {
                return {'invalidDate': true}
            }
        }
        return null;
    }
}
