import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { ICreditContract, ICreditContractList } from '../../interfaces/credit-contract.interfaces';
import { ParserService } from '../utils/parser.service';
import { FormGroup } from '@angular/forms';

@Injectable({
	providedIn: 'root',
})
export class CreditContractService {
	constructor(private http: HttpClient,
                private parserService: ParserService) { }

	fetch(): Observable<ICreditContractList[]> {
		return this.http.get<ICreditContractList[]>('/api/v1/credit_contract/');
	}

	getById(id: number): Observable<ICreditContract> {
        return this.http.get<ICreditContract>(`/api/v1/credit_contract/${id}/`);
    }

    create(formGroup: FormGroup): Observable<ICreditContract> {
        const formData = this.parserService.getValuesFromFormGroup(formGroup);
        return this.http.post<ICreditContract>('/api/v1/credit_contract/', formData);
    }

    payOff(id: number): Observable<ICreditContract> {
        return this.http.put<ICreditContract>(`/api/v1/credit_contract/${id}/pay_off/`, {});
    }
}
