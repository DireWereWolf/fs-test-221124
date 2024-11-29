import { Injectable } from '@angular/core';
import {HttpClient, HttpParams} from '@angular/common/http';
import {environment} from '../../../environments/environment';
import {User} from '../models/user';
import {Observable} from 'rxjs';


interface PaginatedRes {
  items: User[],
  total: number;
}


@Injectable({
  providedIn: 'root'
})
export class UsersHttpService {

  private apiUrl = environment.apiUrl;

  constructor(
    private http: HttpClient
  ) { }

  public getUsers(params: {
    page: number;
    limit: number
  }): Observable<PaginatedRes | User[]>{
    const query = new HttpParams({fromObject: params});

    return this.http.get<PaginatedRes | User[]>(`${this.apiUrl}users`, { params: query });
  }

  public createUser(userData: User): Observable<User> {
    return this.http.post<User>(`${this.apiUrl}user`, userData);
  }

  public getUser(id: string): Observable<User> {
    return this.http.get<User>(`${this.apiUrl}user/${id}`);
  }

  public patchUser(id: string, body: User): Observable<User> {
    return this.http.patch<User>(`${this.apiUrl}user/${id}`, body)
  }

  public deleteUser(id: string) {
    return this.http.delete(`${this.apiUrl}user/${id}`);
  }
}
