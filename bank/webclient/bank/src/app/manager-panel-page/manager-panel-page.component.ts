import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { Observable } from 'rxjs';

import { IBankSettings } from '../shared/interfaces/bank-settings.interfaces';
import { BankSettingsService } from '../shared/services/bank-settings/bank-settings.service';
import { MaterializeService } from '../shared/services/utils/materialize.service';
import {switchMap} from 'rxjs/operators';

@Component({
  selector: 'app-manager-panel-page',
  templateUrl: './manager-panel-page.component.html',
  styleUrls: ['./manager-panel-page.component.css']
})
export class ManagerPanelPageComponent implements OnInit {

    bankSettings: IBankSettings;

	constructor(private router: Router,
				private route: ActivatedRoute,
                private bankSettingsService: BankSettingsService) { }

	ngOnInit(): void {
        this.route.params
			.pipe(
				switchMap(
					(params: Params) => {
                        return this.bankSettingsService.fetch();
					}
				)
			)
			.subscribe(
				(bankSettings: IBankSettings) => {
					if (bankSettings) {
						this.bankSettings = bankSettings;
					}
				},
				error => MaterializeService.toast(error.error),
			);
	}

	onSubmit() {
        let obs$ = this.bankSettingsService.closeDay();
		obs$.subscribe(
            (bankSettings: IBankSettings) => {
                if (bankSettings) {
                    this.bankSettings = bankSettings;
                }
			},
			error => {
				MaterializeService.toast(error.error);
			}
        )
	}
}
