import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs';

import { DepositContractService } from '../shared/services/deposit-contract/deposit-contract.service';
import { IDepositContractList } from '../shared/interfaces/deposit-contract.interfaces';
import { MaterializeService} from '../shared/services/utils/materialize.service';

@Component({
    selector: 'app-deposit-contracts-page',
    templateUrl: './deposit-contracts-page.component.html',
    styleUrls: ['./deposit-contracts-page.component.css']
})
export class DepositContractsPageComponent implements OnInit {

	depositContracts$: Observable<IDepositContractList[]>;

	constructor(private depositContractService: DepositContractService) { }

	ngOnInit(): void {
		this.depositContracts$ = this.depositContractService.fetch();
        this.depositContracts$.subscribe(
            (depositContracts: IDepositContractList[]) => {
			},
			error => {
				MaterializeService.toast(error.error);
			}
        )
	}
}
