import {Component, Input, OnInit} from '@angular/core';
import {Base} from '../../../core/directives/base.directive';
import {UsersHttpService} from '../../services/users-http.service';
import {takeUntil} from 'rxjs';
import {User} from '../../models/user';
import {MatButton, MatButtonModule} from '@angular/material/button';
import {Router} from '@angular/router';
import {CommonModule, NgIf} from '@angular/common';
import {UserCreateEditComponent} from '../user-create-edit/user-create-edit.component';

@Component({
  selector: 'app-user-view',
  imports: [
    MatButtonModule, CommonModule,
    // MatButton,
    NgIf, UserCreateEditComponent
  ],
  templateUrl: './user-view.component.html',
  styleUrl: './user-view.component.scss',
  standalone: true
})
export class UserViewComponent extends Base implements OnInit{

  userData!: User;

  @Input() user_id?: string | null | undefined;

  constructor(
    private _userHttpService: UsersHttpService,
    private _router: Router
  ) {
    super();
  }

  ngOnInit() {
    this.getUser(this.user_id);
  }

  private getUser(id: string | null | undefined) {
    if (!!id) {
      this._userHttpService.getUser(id)
      .pipe(takeUntil(this.destroy$))
      .subscribe(res => {
        this.userData = res;
      })
    }
  }

  public deleteUser() {
    const {user_id} = this.userData;

    if (!!user_id) {
      this._userHttpService.deleteUser(user_id)
      .pipe(takeUntil(this.destroy$))
      .subscribe(() => {
        this._router.navigate(['/']);
      })
    }
  }
}
