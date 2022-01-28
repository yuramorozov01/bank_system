import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

import { IUser, IUserMe, IJWT, IAccess, IRefresh } from '../../interfaces/auth.interfaces';


@Injectable({
	providedIn: 'root'
})
export class AuthService {

	private access: string = null;
	private refresh: string = null;
	private refreshTokenTimeout;

	constructor(private http: HttpClient) {

	}

	register(user: IUser) : Observable<IUser>{
		return this.http.post<IUser>('/auth/users/', user);
	}

	login(user: IUser): Observable<IJWT> {
		return this.http.post<IJWT>('/auth/jwt/create/', user)
			.pipe(
				tap(
					({refresh, access}) => {
						localStorage.setItem('auth-refresh', refresh);
						this.setRefreshToken(refresh);
						localStorage.setItem('auth-token', access);
						this.setAccessToken(access);
						this.startRefreshTokenTimer();
					}
				)
			);
	}

	me(): Observable<IUserMe> {
		return this.http.get<IUserMe>('/auth/users/me/');
	}

	setAccessToken(access: string) {
		this.access = access;
	} 

	getAccessToken(): string {
		return this.access;
	}

	setRefreshToken(refresh: string) {
		this.refresh = refresh;
	} 

	isAuthenticated(): boolean {
		return !!this.access;
	}

	refreshAccessToken(): Observable<IAccess> {
		return this.http.post<IAccess>('/auth/jwt/refresh/', { refresh: this.refresh })
			.pipe(
				tap(
					({access}) => {
						localStorage.setItem('auth-token', access);
						this.setAccessToken(access);
						this.startRefreshTokenTimer();
					}
				)
			);
	}

	logout() {
		this.stopRefreshTokenTimer();
		this.setAccessToken(null);
		this.setRefreshToken(null);
		localStorage.clear();
	}

	startRefreshTokenTimer() {
		const access = JSON.parse(atob(this.access.split('.')[1]));

		const expiresIn = new Date(access.exp * 1000);
		const timeout = expiresIn.getTime() - Date.now() - (60 * 1000);
		this.refreshTokenTimeout = setTimeout(() => this.refreshAccessToken().subscribe(), timeout);
	}

	stopRefreshTokenTimer() {
		clearTimeout(this.refreshTokenTimeout);
	}
}