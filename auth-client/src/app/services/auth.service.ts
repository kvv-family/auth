import { Injectable } from '@angular/core';
import { LocalModel } from '../models/auth';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  localAuth: LocalModel;

  constructor(private http: HttpClient) {
    this.localAuth = new LocalModel(this.http, 'http://localhost:8000');
    this.localAuth.getConfiguration();
  }

  authorizeLocale(username: string, password: string) {
    this.localAuth.authorize(username, password);
  }
}
