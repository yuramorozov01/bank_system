import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';

import { IMessage } from '../../interfaces/utils.interfaces';
import { IClientList, IClient } from '../../interfaces/clients.interfaces';

@Injectable({
	providedIn: 'root',
})
export class ClientService {
	constructor(private http: HttpClient) { }

	fetch(params: any = {}): Observable<IClientList> {
		return this.http.get<IClientList>('/api/v1/client/', {
			params: new HttpParams({
				fromObject: params,
			}),
		});
	}

	getById(id: number): Observable<IClient> {
    return this.http.get<IClient>(`/api/v1/client/${id}/`);
  }
}
