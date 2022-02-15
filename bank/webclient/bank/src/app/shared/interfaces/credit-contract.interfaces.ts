import { IClientList } from './client.interfaces';
import { IBankAccountList } from './bank-account.interfaces';

export interface ICreditTypeList {
	id: number;
    name: string;
    percent: number;
    currency: string;
    credit_term: number;
    is_annuity_payment: boolean;
}

export interface ICreditType {
	id: number;
    name: string;
    percent: number;
    currency: string;
    credit_term: number;
    is_annuity_payment: boolean;
    min_downpayment: number;
    max_downpayment: number;
}

export interface ICreditContractList {
    id: number;
    credit_type: ICreditTypeList;
    starts_at: Date;
    ends_at: Date;
    is_ended: boolean;
    credit_amount: number;
    client: IClientList;
}

export interface ICreditContract {
    id: number;
    credit_type: ICreditTypeList;
    starts_at: Date;
    ends_at: Date;
    is_ended: boolean;
    credit_amount: number;
    client: IClientList;
    main_bank_account: IBankAccountList;
    credit_bank_account: IBankAccountList;
    special_bank_account: IBankAccountList;
}
