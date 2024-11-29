import { Component } from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {NgIf} from '@angular/common';
import {UserCreateEditComponent} from '../../users/components/user-create-edit/user-create-edit.component';
import {MatCard, MatCardContent} from '@angular/material/card';
import {UserViewComponent} from '../../users/components/user-view/user-view.component';

@Component({
  selector: 'app-user-page',
  imports: [
    NgIf,
    UserCreateEditComponent,
    UserViewComponent
  ],
  templateUrl: './user-page.component.html',
  styleUrl: './user-page.component.scss',
  standalone: true
})
export class UserPageComponent {
  userId: string | null = null;
  currentViewMode: 'create' | 'view' = 'create';

  constructor(
    private route: ActivatedRoute,
  ) {}

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {
      this.userId = params.get('id') ?? null;

      if (this.userId) {
        this.currentViewMode = 'view';
      } else {
        this.currentViewMode = 'create'
      }

    });
  }
}
