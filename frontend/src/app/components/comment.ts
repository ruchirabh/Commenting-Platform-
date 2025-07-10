import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_CONFIG } from '../core/api.config';

@Injectable({
  providedIn: 'root'
})
export class CommentService {
  constructor(private http: HttpClient) {}

  private getAuthHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  getComments(limit: number = 10, skip: number = 0): Observable<any> {
    return this.http.get(`${API_CONFIG.COMMENTS.BASE}?limit=${limit}&skip=${skip}`, {
      headers: this.getAuthHeaders()
    });
  }

  createComment(content: string, parentId?: string): Observable<any> {
    const body = parentId ? { content, parent_id: parentId } : { content };
    return this.http.post(API_CONFIG.COMMENTS.CREATE, body, {
      headers: this.getAuthHeaders()
    });
  }

  updateComment(commentId: string, content: string): Observable<any> {
    return this.http.put(`${API_CONFIG.COMMENTS.BASE}/${commentId}`, { content }, {
      headers: this.getAuthHeaders()
    });
  }

  deleteComment(commentId: string): Observable<any> {
    return this.http.delete(`${API_CONFIG.COMMENTS.BASE}/${commentId}`, {
      headers: this.getAuthHeaders()
    });
  }

  likeComment(commentId: string): Observable<any> {
    return this.http.post(`${API_CONFIG.COMMENTS.BASE}/${commentId}/like`, {}, {
      headers: this.getAuthHeaders()
    });
  }

  getReplies(commentId: string, limit: number = 10, skip: number = 0): Observable<any> {
    return this.http.get(
      `${API_CONFIG.COMMENTS.BASE}/${commentId}/replies?limit=${limit}&skip=${skip}`,
      { headers: this.getAuthHeaders() }
    );
  }
}