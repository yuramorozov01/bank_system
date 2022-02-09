import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs';

import { DepositTypeService } from '../../shared/services/deposit/deposit_type/deposit_type.service';
import { IDepositTypeList } from '../../shared/interfaces/deposit.interfaces'
import { MaterializeService} from '../../shared/services/utils/materialize.service';

@Component({
  selector: 'app-deposit-types-page',
  templateUrl: './deposit-types-page.component.html',
  styleUrls: ['./deposit-types-page.component.css']
})
export class DepositTypesPageComponent implements OnInit {

	deposit_types$: Observable<IDepositTypeList[]>;

	constructor(private depositTypeService: DepositTypeService) { }

	ngOnInit(): void {
		this.deposit_types$ = this.depositTypeService.fetch();
        this.deposit_types$.subscribe(
            (deposit_types: IDepositTypeList[]) => {
			},
			error => {
				MaterializeService.toast(error.error);
			}
        )
	}

}

