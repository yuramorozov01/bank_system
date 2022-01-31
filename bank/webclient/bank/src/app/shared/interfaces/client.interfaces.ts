export interface IClientList {
	id: number;
  last_name: string;
  first_name: string;
  patronymic: string;

  birthday: Date;
  sex: string;

  passport_series: string;
  passport_number: string;
  id_number: string;
}

export interface IClient {
	id: number;
  last_name: string;
  first_name: string;
  patronymic: string;

  birthday: Date;
  birthday_place: string;
  sex: string;

  passport_series: string;
  passport_number: string;
  passport_issued_by: string;
  passport_issued_at: Date;
  id_number: string;

  city: string;
  address: string;

  home_number: string;
  phone_number: string;

  email: string;

  job_place: string;
  job_position: string;

  register_city: string;
  register_address: string;

  family_status: string;
  citizen: string;
  disability: number;
  pensioner: boolean;
  monthly_salary: number;
  army: boolean;
}
