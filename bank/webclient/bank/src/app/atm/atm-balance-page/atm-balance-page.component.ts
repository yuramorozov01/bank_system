import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { switchMap } from 'rxjs/operators';

import { IReceipt } from '../../shared/interfaces/utils.interfaces';

import { AtmService } from '../../shared/services/atm/atm-service';
import { MaterializeService } from '../../shared/services/utils/materialize.service';


@Component({
  selector: 'app-atm-balance-page',
  templateUrl: './atm-balance-page.component.html',
  styleUrls: ['./atm-balance-page.component.css']
})
export class AtmBalancePageComponent implements OnInit {
    @ViewChild('pdfReceipt', {static: false}) pdfReceipt: ElementRef;

	balanceReceipt: IReceipt;

	constructor(private router: Router,
				private route: ActivatedRoute,
				private atmService: AtmService) { }

	ngOnInit(): void {
        this.refreshBalance();
	}

    refreshBalance(): void {
        this.route.params
			.pipe(
				switchMap(
					(params: Params) => {
                        return this.atmService.balance();
					}
				)
			)
			.subscribe(
				(balanceReceipt: IReceipt) => {
					if (balanceReceipt) {
						this.balanceReceipt = balanceReceipt;
					}
				},
                error => MaterializeService.toast(error.error),
			);
    }

	printReceipt() {
        this.atmService.printReceipt(this.pdfReceipt);
	}
}
