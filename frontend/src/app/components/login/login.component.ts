import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { User } from '../../models/user';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  user: User = new User();

  constructor(private router: Router, private auth: AuthService) { }

  onLogin(): void {
    this.auth.login(this.user).then((user) => {
      localStorage.setItem('token', user.auth_token);
      this.router.navigateByUrl('/status');
    }).catch((err) => {
      console.log(err);
    });
  }
}
