import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs';

import { BankAccountService } from '../shared/services/bank-account/bank-account.service';
import { IBankAccountList } from '../shared/interfaces/bank-account.interfaces';
import { MaterializeService} from '../shared/services/utils/materialize.service';

@Component({
	selector: 'app-bank-accounts-page',
	templateUrl: './bank-accounts-page.component.html',
	styleUrls: ['./bank-accounts-page.component.css']
})
export class BankAccountsPageComponent implements OnInit {

	bankAccounts$: Observable<IBankAccountList[]>;

	constructor(private bankAccountService: BankAccountService) { }

	ngOnInit(): void {
		this.bankAccounts$ = this.bankAccountService.fetch();
        this.bankAccounts$.subscribe(
            (bankAccounts: IBankAccountList[]) => {
			},
			error => {
				MaterializeService.toast(error.error);
			}
        )
	}

}
