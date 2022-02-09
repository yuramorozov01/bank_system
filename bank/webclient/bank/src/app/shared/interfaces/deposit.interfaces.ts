import { IClientList } from './client.interfaces';

export interface IDepositTypeList {
	id: number;
    name: string;
    percent: number;
    currency: string;
    deposit_term: number;
    is_revocable: boolean;
}

export interface IDepositType {
	id: number;
    name: string;
    percent: number;
    currency: string;
    deposit_term: number;
    is_revocable: boolean;
    min_downpayment: number;
    max_downpayment: number;
}
