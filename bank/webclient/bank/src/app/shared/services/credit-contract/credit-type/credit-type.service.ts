import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';

import { IMessage } from '../../../interfaces/utils.interfaces';
import { ICreditType, ICreditTypeList } from '../../../interfaces/credit-contract.interfaces';
import { ParserService } from '../../utils/parser.service';
import { FormGroup } from '@angular/forms';

@Injectable({
	providedIn: 'root',
})
export class CreditTypeService {
	constructor(private http: HttpClient,
                private parserService: ParserService) { }

	fetch(): Observable<ICreditTypeList[]> {
		return this.http.get<ICreditTypeList[]>('/api/v1/credit_type/');
	}

	getById(id: number): Observable<ICreditType> {
        return this.http.get<ICreditType>(`/api/v1/credit_type/${id}/`);
    }

    create(formGroup: FormGroup): Observable<ICreditType> {
        const formData = this.parserService.getValuesFromFormGroup(formGroup);
        return this.http.post<ICreditType>('/api/v1/credit_type/', formData);
    }

    update(id: number, formGroup: FormGroup): Observable<ICreditType> {
        const formData = this.parserService.getValuesFromFormGroup(formGroup);
        return this.http.put<ICreditType>(`/api/v1/credit_type/${id}/`, formData);
    }

    delete(id: number): Observable<IMessage> {
        return this.http.delete<IMessage>(`/api/v1/credit_type/${id}/`);
    }
}
