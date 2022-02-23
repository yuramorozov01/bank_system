import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router, ActivatedRoute, Params } from '@angular/router';
import { FormGroup, FormControl, Validators } from '@angular/forms';
import { switchMap } from 'rxjs/operators';

import { IReceipt } from '../../shared/interfaces/utils.interfaces';

import { AtmService } from '../../shared/services/atm/atm-service';
import { MaterializeService } from '../../shared/services/utils/materialize.service';

@Component({
  selector: 'app-atm-withdraw-page',
  templateUrl: './atm-withdraw-page.component.html',
  styleUrls: ['./atm-withdraw-page.component.css']
})
export class AtmWithdrawPageComponent implements OnInit {
    @ViewChild('pdfReceipt', {static: false}) pdfReceipt: ElementRef;

    form: FormGroup;

	withdrawReceipt: IReceipt;

	constructor(private router: Router,
				private route: ActivatedRoute,
				private atmService: AtmService) { }

	ngOnInit(): void {
        this.form = new FormGroup({
            amount: new FormControl(null, [Validators.required, Validators.min(0)]),
		});
	}

    onSubmit() {
		let obs$;
		this.form.disable();
        obs$ = this.atmService.withdraw(this.form);
		obs$.subscribe(
			(withdrawReceipt: IReceipt) => {
				this.withdrawReceipt = withdrawReceipt;
				MaterializeService.toast({'Success': 'Balance has been withdrawn!'});
				this.form.enable();
			},
			error => {
				MaterializeService.toast(error.error);
				this.form.enable();
			}
		);
	}

	printReceipt() {
        this.atmService.printReceipt(this.pdfReceipt);
	}
}
