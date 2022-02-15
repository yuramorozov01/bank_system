import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs';

import { CreditTypeService } from '../../shared/services/credit-contract/credit-type/credit-type.service';
import { ICreditTypeList } from '../../shared/interfaces/credit-contract.interfaces'
import { MaterializeService} from '../../shared/services/utils/materialize.service';

@Component({
  selector: 'app-credit-types-page',
  templateUrl: './credit-types-page.component.html',
  styleUrls: ['./credit-types-page.component.css']
})
export class CreditTypesPageComponent implements OnInit {

	creditTypes$: Observable<ICreditTypeList[]>;

	constructor(private creditTypeService: CreditTypeService) { }

	ngOnInit(): void {
		this.creditTypes$ = this.creditTypeService.fetch();
        this.creditTypes$.subscribe(
            (creditTypes: ICreditTypeList[]) => {
			},
			error => {
				MaterializeService.toast(error.error);
			}
        )
	}

}

