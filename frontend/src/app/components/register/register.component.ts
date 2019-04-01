import { Component, OnInit } from '@angular/core';
import { User } from '../../models/user';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { UserAccount } from '../../models/user-account';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  user: User = new User();
  userAccount: UserAccount = new UserAccount();

  constructor(private router: Router, private auth: AuthService) { }

  onRegister(): void {
    this.auth.register(this.userAccount).then((response) => {
      localStorage.setItem('token', response.auth_token);
      this.router.navigateByUrl('/status');
    }).catch((err) => {
      console.log(err);
    });
  }
}
