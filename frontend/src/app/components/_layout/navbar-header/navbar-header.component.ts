import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-navbar-header',
  templateUrl: './navbar-header.component.html',
  styleUrls: ['./navbar-header.component.css']
})
export class NavbarHeaderComponent implements OnInit {

  constructor(private router: Router, private auth: AuthService) { }

  ngOnInit() {
  }

  onLogout(): void {
    this.auth.logout(localStorage.getItem('token'))
    .then((response) => {
      console.log(response);
      localStorage.removeItem('token');
      this.router.navigateByUrl('/login');
    }).catch((err) => {
      console.log(err);
    });
  }

}
