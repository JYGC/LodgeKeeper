import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-status',
  templateUrl: './status.component.html',
  styleUrls: ['./status.component.css']
})
export class StatusComponent implements OnInit {
  isLoggedIn = false;

  constructor(private router: Router, private auth: AuthService) { }

  ngOnInit(): void {
    const token = localStorage.getItem('token');
    if (token) {
      this.auth.ensureAuthenticated(token).then((user) => {
        console.log(user);
        if (user.status === 'success') {
          this.isLoggedIn = true;
        }
      }).catch((err) => {
        console.log(err);
      });
    }
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
