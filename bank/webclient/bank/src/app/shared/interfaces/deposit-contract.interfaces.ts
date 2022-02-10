import { IClientList } from './client.interfaces';
import { IBankAccountList } from './bank-account.interfaces';

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

export interface IDepositContractList {
    id: number;
    deposit_type: IDepositTypeList;
    starts_at: Date;
    ends_at: Date;
    is_ended: boolean;
    deposit_amount: number;
    client: IClientList;
}

export interface IDepositContract {
    id: number;
    deposit_type: IDepositTypeList;
    starts_at: Date;
    ends_at: Date;
    is_ended: boolean;
    deposit_amount: number;
    client: IClientList;
    main_bank_account: IBankAccountList;
    deposit_bank_account: IBankAccountList;
    special_bank_account: IBankAccountList;
}
