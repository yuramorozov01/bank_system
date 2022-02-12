import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { FormGroup } from '@angular/forms';
import { Observable } from 'rxjs';

import { IBankSettings } from '../shared/interfaces/bank-settings.interfaces';
import { BankSettingsService } from '../shared/services/bank-settings/bank-settings.service';
import { MaterializeService } from '../shared/services/utils/materialize.service';

@Component({
  selector: 'app-manager-panel-page',
  templateUrl: './manager-panel-page.component.html',
  styleUrls: ['./manager-panel-page.component.css']
})
export class ManagerPanelPageComponent implements OnInit {
	@ViewChild('input') inputRef: ElementRef;

	form: FormGroup;
	isNew = true;
	bankSettings$: Observable<IBankSettings>;

	constructor(private router: Router,
				private route: ActivatedRoute,
                private bankSettingsService: BankSettingsService) { }

	ngOnInit(): void {
        this.bankSettings$ = this.bankSettingsService.fetch();
        this.bankSettings$.subscribe(
            (bankSettings: IBankSettings) => {
			},
			error => {
				MaterializeService.toast(error.error);
			}
        )
	}

	triggerClick() {
		this.inputRef.nativeElement.click();
	}

	onSubmit() {
		let obs$;
		this.form.disable();

        this.bankSettings$ = this.bankSettingsService.close_day();
		this.bankSettings$.subscribe(
            (bankSettings: IBankSettings) => {
			},
			error => {
				MaterializeService.toast(error.error);
			}
        )
	}
}
