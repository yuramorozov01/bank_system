import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-atm-auth-layout',
  templateUrl: './atm-auth-layout.component.html',
  styleUrls: ['./atm-auth-layout.component.css']
})
export class AtmAuthLayoutComponent implements OnInit {
	links = [
        {
            url: '/login',
            name: 'Bank',
        },
        {
			url: '/atm/login',
			name: 'Login',
		},
	];

  constructor() { }

  ngOnInit(): void {
  }

}
