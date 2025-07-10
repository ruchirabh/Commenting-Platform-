import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_CONFIG } from '../core/api.config';
import { HttpParams, HttpHeaders } from '@angular/common/http';
@Injectable({
  providedIn: 'root',
})
export class Auth {
  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  }
  constructor(private http: HttpClient) {}
  signup(userData: any): Observable<any> {
    return this.http.post(API_CONFIG.USER.SIGNUP, userData);
  }
  login(userData: any): Observable<any> {
    const body = new HttpParams()
      .set('username', userData.username)
      .set('password', userData.password);

    const headers = new HttpHeaders({
      'Content-Type': 'application/x-www-form-urlencoded',
    });

    return this.http.post(API_CONFIG.USER.LOGIN, body.toString(), { headers });
  }
  resetPassword(resetData: {
    email: string;
    new_password: string;
  }): Observable<any> {
    return this.http.post(API_CONFIG.USER.RESET_PASSWORD, resetData);
  }
  private getAuthHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
  }

  uploadProfilePicture(file: File): Observable<any> {
  const formData = new FormData();
  formData.append('file', file);

  const headers = this.getAuthHeaders(); 

  return this.http.post(API_CONFIG.USER.PROFILE_PIC, formData, { headers });
}


  getProfilePicture(userId?: string): Observable<Blob> {
    const url = userId ? 
      `${API_CONFIG.USER.PROFILE_PIC}?user_id=${userId}` : 
      API_CONFIG.USER.PROFILE_PIC;
      
    return this.http.get(url, {
      responseType: 'blob',
      headers: this.getAuthHeaders()  
    });
  }

  getUserProfile(): Observable<any> {
    return this.http.get(API_CONFIG.USER.ME);
  }
  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }
  getCurrentUser(): any {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  }
}
