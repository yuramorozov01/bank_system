import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';

import { Observable } from 'rxjs';

import { IBankSettings } from '../../interfaces/bank-settings.interfaces';

@Injectable({
	providedIn: 'root',
})
export class BankSettingsService {
	constructor(private http: HttpClient) { }

	fetch(): Observable<IBankSettings> {
		return this.http.get<IBankSettings>('/api/v1/bank_settings/');
	}

    closeDay(): Observable<IBankSettings> {
        return this.http.put<IBankSettings>('/api/v1/bank_settings/close_day/', {});
    }
}
