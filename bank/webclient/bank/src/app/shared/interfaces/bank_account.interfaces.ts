import { IClientList } from './client.interfaces';

export interface IBankAccountList {
	id: number;
    number: string;
    activity_type: string;
    bank_account_type: string;
    balance: number;
    client: IClientList;
}

export interface IBankAccount {
    id: number;
    number: string;
    activity_type: string;
    bank_account_type: string;
    balance: number;
    client: IClientList;
}
