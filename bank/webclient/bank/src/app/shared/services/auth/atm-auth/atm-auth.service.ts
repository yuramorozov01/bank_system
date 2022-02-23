import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

import { IAccess } from '../../../interfaces/auth.interfaces';
import { ParserService } from '../../utils/parser.service';
import { FormGroup } from '@angular/forms';


@Injectable({
	providedIn: 'root'
})
export class AtmAuthService {

	private access: string = null;

	constructor(private http: HttpClient,
                private parserService: ParserService) {

	}

	auth(formGroup: FormGroup) : Observable<IAccess>{
        const formData = this.parserService.getValuesFromFormGroup(formGroup);
		return this.http.post<IAccess>('/api/v1/bank_card/auth/', formData)
            .pipe(
                tap(
                    ({access}) => {
                        localStorage.setItem('bank-card-auth-token', access);
                        this.setAccessToken(access);
                    }
                )
            );
	}

	setAccessToken(access: string) {
		this.access = access;
	}

	getAccessToken(): string {
		return this.access;
	}

	isAuthenticated(): boolean {
		return !!this.access;
	}

	logout() {
		this.setAccessToken(null);
        localStorage.removeItem('bank-card-auth-token')
	}
}
