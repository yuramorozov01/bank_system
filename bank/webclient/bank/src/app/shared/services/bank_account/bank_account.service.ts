import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';

import { IBankAccountList, IBankAccount } from '../../interfaces/bank_account.interfaces';

@Injectable({
	providedIn: 'root',
})
export class BankAccountService {
	constructor(private http: HttpClient) { }

	fetch(): Observable<IBankAccountList[]> {
		return this.http.get<IBankAccountList[]>('/api/v1/bank_account/');
	}

	getById(id: number): Observable<IBankAccount> {
        return this.http.get<IBankAccount>(`/api/v1/bank_account/${id}/`);
    }
}
