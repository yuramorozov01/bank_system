import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';

import { IMessage } from '../../../interfaces/utils.interfaces';
import { IDepositType, IDepositTypeList } from '../../../interfaces/deposit.interfaces';
import { ParserService } from '../../utils/parser.service';
import { FormGroup } from '@angular/forms';

@Injectable({
	providedIn: 'root',
})
export class DepositTypeService {
	constructor(private http: HttpClient,
                private parserService: ParserService) { }

	fetch(): Observable<IDepositTypeList[]> {
		return this.http.get<IDepositTypeList[]>('/api/v1/deposit_type/');
	}

	getById(id: number): Observable<IDepositType> {
        return this.http.get<IDepositType>(`/api/v1/deposit_type/${id}/`);
    }

    create(formGroup: FormGroup): Observable<IDepositType> {
        const formData = this.parserService.getValuesFromFormGroup(formGroup);
        return this.http.post<IDepositType>('/api/v1/deposit_type/', formData);
    }

    update(id: number, formGroup: FormGroup): Observable<IDepositType> {
        const formData = this.parserService.getValuesFromFormGroup(formGroup);
        return this.http.put<IDepositType>(`/api/v1/deposit_type/${id}/`, formData);
    }

    delete(id: number): Observable<IMessage> {
        return this.http.delete<IMessage>(`/api/v1/deposit_type/${id}/`);
    }
}
