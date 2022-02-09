import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { IBankAccountList, IBankAccount } from '../../interfaces/bank-account.interfaces';
import { FormGroup } from '@angular/forms';
import { ParserService } from '../utils/parser.service';

@Injectable({
	providedIn: 'root',
})
export class BankAccountService {
	constructor(private http: HttpClient,
                private parserService: ParserService) { }

	fetch(): Observable<IBankAccountList[]> {
		return this.http.get<IBankAccountList[]>('/api/v1/bank_account/');
	}

	getById(id: number): Observable<IBankAccount> {
        return this.http.get<IBankAccount>(`/api/v1/bank_account/${id}/`);
    }

    topUp(id: number, formGroup: FormGroup): Observable<IBankAccount> {
        const formData = this.parserService.getValuesFromFormGroup(formGroup);
        return this.http.put<IBankAccount>(`/api/v1/bank_account/${id}/top_up/`, formData);
    }
}
