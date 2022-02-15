import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs';

import { CreditContractService } from '../shared/services/credit-contract/credit-contract.service';
import { ICreditContractList } from '../shared/interfaces/credit-contract.interfaces';
import { MaterializeService} from '../shared/services/utils/materialize.service';

@Component({
    selector: 'app-credit-contracts-page',
    templateUrl: './credit-contracts-page.component.html',
    styleUrls: ['./credit-contracts-page.component.css']
})
export class CreditContractsPageComponent implements OnInit {

	creditContracts$: Observable<ICreditContractList[]>;

	constructor(private creditContractService: CreditContractService) { }

	ngOnInit(): void {
		this.creditContracts$ = this.creditContractService.fetch();
        this.creditContracts$.subscribe(
            (creditContracts: ICreditContractList[]) => {
			},
			error => {
				MaterializeService.toast(error.error);
			}
        )
	}
}
