import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from './auth.service';

@Injectable()
export class EnsureAuthenticated implements CanActivate {
  constructor(private auth: AuthService, private router: Router) {}

  canActivate(): Promise<boolean> | boolean {
    const token = localStorage.getItem('token');
    if (token) {
      return this.auth.ensureAuthenticated(token)
      .then((response) => {
        return true;
      })
      .catch((error) => {
        this.router.navigateByUrl('/login');
        return false;
      });
    } else {
      this.router.navigateByUrl('/login');
      return false;
    }
  }
}
