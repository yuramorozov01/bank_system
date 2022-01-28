import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';

import { IMessage } from '../../interfaces/utils.interfaces';
import { IClientList, IClient } from '../../interfaces/client.interfaces';

@Injectable({
	providedIn: 'root',
})
export class ClientService {
	constructor(private http: HttpClient) { }

	fetch(): Observable<IClientList[]> {
		return this.http.get<IClientList[]>('/api/v1/client/');
	}

	getById(id: number): Observable<IClient> {
    return this.http.get<IClient>(`/api/v1/client/${id}/`);
  }

  create(description: string, expireDate: Date): Observable<IClient> {
		const formData = new FormData();
		formData.append('description', description);
		formData.append('expireDate', expireDate.toDateString());

		return this.http.post<IClient>('/api/v1/client/', formData);
	}

	update(id: string, description: string, expireDate: Date): Observable<IClient> {
		const formData = new FormData();
		formData.append('description', description);
		formData.append('expireDate', expireDate.toDateString());

		return this.http.patch<IClient>(`/api/v1/client/${id}/`, formData);
	}

  delete(id: string): Observable<IMessage> {
		return this.http.delete<IMessage>(`/api/v1/client/${id}/`);
	}
}
