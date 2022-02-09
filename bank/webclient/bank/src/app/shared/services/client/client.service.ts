import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';

import { IMessage } from '../../interfaces/utils.interfaces';
import { IClientList, IClient } from '../../interfaces/client.interfaces';
import { ParserService } from '../utils/parser.service';
import { FormGroup } from '@angular/forms';

@Injectable({
	providedIn: 'root',
})
export class ClientService {
	constructor(private http: HttpClient,
                private parserService: ParserService) { }

	fetch(): Observable<IClientList[]> {
		return this.http.get<IClientList[]>('/api/v1/client/');
	}

	getById(id: number): Observable<IClient> {
        return this.http.get<IClient>(`/api/v1/client/${id}/`);
    }

    create(formGroup: FormGroup): Observable<IClient> {
        const formData = this.parserService.getValuesFromFormGroup(formGroup);
        return this.http.post<IClient>('/api/v1/client/', formData);
    }

    update(id: number, formGroup: FormGroup): Observable<IClient> {
        const formData = this.parserService.getValuesFromFormGroup(formGroup);
        return this.http.put<IClient>(`/api/v1/client/${id}/`, formData);
    }

    delete(id: number): Observable<IMessage> {
        return this.http.delete<IMessage>(`/api/v1/client/${id}/`);
    }
}
