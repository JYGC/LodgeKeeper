import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';
import { Router, CanActivate } from '@angular/router';

@Injectable()
export class LoginRedirect implements CanActivate {
  constructor(private auth: AuthService, private router: Router) {}

  canActivate(): Promise<boolean> | boolean {
    const token = localStorage.getItem('token');
    if (token) {
      return this.auth.ensureAuthenticated(token)
      .then((response) => {
        this.router.navigateByUrl('/dashboard');
        return false;
      })
      .catch((error) => {
        return true;
      });
    } else {
      return true;
    }
  }
}
