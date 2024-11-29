import { Component } from '@angular/core';
import {MatPaginator, PageEvent} from '@angular/material/paginator';
import {UsersHttpService} from '../../services/users-http.service';
import {User} from '../../models/user';
import {NgForOf} from '@angular/common';
import {RouterLink} from '@angular/router';

@Component({
  selector: 'app-users-list',
  imports: [
    MatPaginator,
    NgForOf,
    RouterLink
  ],
  templateUrl: './users-list.component.html',
  styleUrl: './users-list.component.scss',
  standalone: true
})
export class UsersListComponent {

  paginationSettings = {
    page: 1, // current page
    limit: 5, // per page
    total: 0
  }
  paginatedItems: User[] = [];

  constructor(
    private usersHttpService: UsersHttpService
  ) {}

  ngOnInit() {
    this.getUsers();
  }

  getUsers() {
    this.usersHttpService.getUsers({
      page: this.paginationSettings.page,
      limit: this.paginationSettings.limit
    }).subscribe(res => {
      if (Array.isArray(res)) {
        this.paginatedItems = res as User[];
      } else {
        this.paginatedItems = res.items;
        this.paginationSettings.total = res.total;
      }
    })
  }

  handlePageEvent(e: PageEvent) {
    this.paginationSettings.page = e.pageIndex + 1;
    this.getUsers();
  }
}
