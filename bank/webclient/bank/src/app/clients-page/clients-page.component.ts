import { Component, OnInit } from '@angular/core';

import { Observable } from 'rxjs';

import { ClientService } from '../shared/services/client/client.service';
import { IClientList } from '../shared/interfaces/client.interfaces';
import { MaterializeService} from '../shared/services/utils/materialize.service';

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
        this.clients$.subscribe(
            (clients: IClientList[]) => {
			},
			error => {
				MaterializeService.toast(error.error);
			}
        )
	}

}
