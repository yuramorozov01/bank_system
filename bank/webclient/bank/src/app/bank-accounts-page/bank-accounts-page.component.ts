import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs';

import { BankAccountService } from '../shared/services/bank_account/bank_account.service';
import { IBankAccountList } from '../shared/interfaces/bank_account.interfaces';
import { MaterializeService} from '../shared/services/utils/materialize.service';

@Component({
	selector: 'app-bank-accounts-page',
	templateUrl: './bank-accounts-page.component.html',
	styleUrls: ['./bank-accounts-page.component.css']
})
export class BankAccountsPageComponent implements OnInit {

	bank_accounts$: Observable<IBankAccountList[]>;

	constructor(private bankAccountService: BankAccountService) { }

	ngOnInit(): void {
		this.bank_accounts$ = this.bankAccountService.fetch();
        this.bank_accounts$.subscribe(
            (bank_accounts: IBankAccountList[]) => {
			},
			error => {
				MaterializeService.toast(error.error);
			}
        )
	}

}
