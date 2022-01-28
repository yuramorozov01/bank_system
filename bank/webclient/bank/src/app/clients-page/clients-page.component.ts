import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs';

import { ClientService } from '../shared/services/client/client.service';
import { IClientList } from '../shared/interfaces/client.interfaces';

@Component({
	selector: 'app-clients-page',
	templateUrl: './clients-page.component.html',
	styleUrls: ['./clients-page.component.css']
})
export class ClientsPageComponent implements OnInit {

	clients$: Observable<IClientList[]>;

	constructor(private clientService: ClientService) { }

	ngOnInit(): void {
		this.clients$ = this.clientService.fetch();
	}

}
