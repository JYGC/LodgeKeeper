import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { User } from '../models/user';
import { UserAccount } from '../models/user-account';

@Injectable()
export class AuthService {
  private BASE_URL = 'http://localhost:5000/auth';

  private headers: HttpHeaders = new HttpHeaders({
    'Content-Type':
    'application/json'
  });

  constructor(private http: HttpClient) { }

  login(user: User): Promise<any> {
    const url = `${this.BASE_URL}/login`;
    return this.http.post(url, user, { headers: this.headers }).toPromise();
  }

  register(userAccount: UserAccount): Promise<any> {
    const url = `${this.BASE_URL}/register`;
    return this.http.post(url, userAccount, { headers: this.headers })
      .toPromise();
  }

  ensureAuthenticated(token): Promise<any> {
    const url = `${this.BASE_URL}/status`;

    const headers: HttpHeaders = new HttpHeaders({
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    });

    return this.http.get(url, { headers }).toPromise();
  }
}
