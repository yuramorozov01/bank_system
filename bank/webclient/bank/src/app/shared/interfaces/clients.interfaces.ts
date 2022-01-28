export interface IClientList {
	id: number;
	title: string;
	tagline: string;
	category?: number;
	rating_user: boolean;
	middle_star: number;
	poster: string;
}

export interface IClient {
	id: number;
	category: string;
	genres: string[];
}
