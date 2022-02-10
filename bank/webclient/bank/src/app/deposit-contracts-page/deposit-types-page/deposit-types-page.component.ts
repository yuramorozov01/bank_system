import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs';

import { DepositTypeService } from '../../shared/services/deposit-contract/deposit-type/deposit-type.service';
import { IDepositTypeList } from '../../shared/interfaces/deposit-contract.interfaces'
import { MaterializeService} from '../../shared/services/utils/materialize.service';

@Component({
  selector: 'app-deposit-types-page',
  templateUrl: './deposit-types-page.component.html',
  styleUrls: ['./deposit-types-page.component.css']
})
export class DepositTypesPageComponent implements OnInit {

	depositTypes$: Observable<IDepositTypeList[]>;

	constructor(private depositTypeService: DepositTypeService) { }

	ngOnInit(): void {
		this.depositTypes$ = this.depositTypeService.fetch();
        this.depositTypes$.subscribe(
            (deposit_types: IDepositTypeList[]) => {
			},
			error => {
				MaterializeService.toast(error.error);
			}
        )
	}

}

