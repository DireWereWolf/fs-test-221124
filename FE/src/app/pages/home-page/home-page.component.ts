import { Component } from '@angular/core';
import {UsersListComponent} from '../../users/components/users-list/users-list.component';
import {MatButton} from '@angular/material/button';
import {RouterLink} from '@angular/router';

@Component({
  selector: 'app-home-page',
  imports: [
    UsersListComponent,
    MatButton,
    RouterLink
  ],
  templateUrl: './home-page.component.html',
  styleUrl: './home-page.component.scss',
  standalone: true
})
export class HomePageComponent {

}
