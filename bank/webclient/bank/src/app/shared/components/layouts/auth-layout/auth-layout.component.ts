import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-auth-layout',
  templateUrl: './auth-layout.component.html',
  styleUrls: ['./auth-layout.component.css']
})
export class AuthLayoutComponent implements OnInit {

	links = [
        {
            url: '/atm',
            name: 'ATM',
        },
		{
			url: '/login',
			name: 'Login',
		},
		{
			url: '/register',
			name: 'Register',
		},
	];

  constructor() { }

  ngOnInit(): void {
  }

}
