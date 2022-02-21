import { IClientList } from './client.interfaces';
import { IBankCardList } from './bank-card.interfaces';

export interface IBankAccountList {
	id: number;
    number: string;
    activity_type: string;
    bank_account_type: string;
    balance: number;
    client: IClientList;
    bank_cards: IBankCardList[];
}

export interface IBankAccount {
    id: number;
    number: string;
    activity_type: string;
    bank_account_type: string;
    balance: number;
    client: IClientList;
    bank_cards: IBankCardList[];
}
