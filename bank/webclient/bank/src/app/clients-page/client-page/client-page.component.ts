import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { FormGroup, FormControl, Validators } from '@angular/forms';

import { switchMap } from 'rxjs/operators';
import { of } from 'rxjs';

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

    sex_values = {
        'Male': 'Male',
        'Female': 'Female',
        'X': 'X',
    };

	constructor(private router: Router,
				private route: ActivatedRoute,
				private clientService: ClientService) { }

	ngOnInit(): void {
        this.form = new FormGroup({
            last_name: new FormControl(null, Validators.required),
            first_name: new FormControl(null, Validators.required),
            patronymic: new FormControl(null, Validators.required),

            birthday: new FormControl(null, Validators.required),
            birthday_place: new FormControl(null, Validators.required),
            sex: new FormControl(null, Validators.required),

            passport_series: new FormControl(null, Validators.required),
            passport_number: new FormControl(null, Validators.required),
            passport_issued_by: new FormControl(null, Validators.required),
            passport_issued_at: new FormControl(null, Validators.required),
            id_number: new FormControl(null, Validators.required),

            city: new FormControl(null, Validators.required),
            address: new FormControl(null, Validators.required),

            home_number: new FormControl(),
            phone_number: new FormControl(),

            email: new FormControl(null, Validators.email),

            job_place: new FormControl(),
            job_position: new FormControl(),

            register_city: new FormControl(null, Validators.required),
            register_address: new FormControl(null, Validators.required),

            family_status: new FormControl(null, Validators.required),
            citizen: new FormControl(null, Validators.required),
            disability: new FormControl(null, Validators.required),
            pensioner: new FormControl(null, Validators.required),
            monthly_salary: new FormControl(null),
            army: new FormControl(null, Validators.required),
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

}
