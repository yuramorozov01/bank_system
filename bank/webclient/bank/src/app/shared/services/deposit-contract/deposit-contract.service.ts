import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { IDepositContract, IDepositContractList } from '../../interfaces/deposit-contract.interfaces';
import { ParserService } from '../utils/parser.service';
import { FormGroup } from '@angular/forms';

@Injectable({
	providedIn: 'root',
})
export class DepositContractService {
	constructor(private http: HttpClient,
                private parserService: ParserService) { }

	fetch(): Observable<IDepositContractList[]> {
		return this.http.get<IDepositContractList[]>('/api/v1/deposit_contract/');
	}

	getById(id: number): Observable<IDepositContract> {
        return this.http.get<IDepositContract>(`/api/v1/deposit_contract/${id}/`);
    }

    create(formGroup: FormGroup): Observable<IDepositContract> {
        const formData = this.parserService.getValuesFromFormGroup(formGroup);
        return this.http.post<IDepositContract>('/api/v1/deposit_contract/', formData);
    }

    revoke(id: number): Observable<IDepositContract> {
        return this.http.put<IDepositContract>(`/api/v1/deposit_contract/${id}/revoke/`, {});
    }
}
