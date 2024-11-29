import {Component, Input, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from '@angular/forms';
import {MatError, MatFormField} from '@angular/material/form-field';
import {MatInput} from '@angular/material/input';
import {MatLabel} from '@angular/material/form-field';
import {CommonModule} from '@angular/common';
import {MatList, MatListItem} from '@angular/material/list';
import {MatButton} from '@angular/material/button';
import {UsersHttpService} from '../../services/users-http.service';
import {User} from '../../models/user';
import {Base} from '../../../core/directives/base.directive';
import {takeUntil} from 'rxjs';
import {Router} from '@angular/router';

@Component({
  selector: 'app-user-create-edit',
  imports: [
    MatFormField,
    MatInput,
    MatLabel,
    ReactiveFormsModule,
    CommonModule,
    MatError,
    MatButton
  ],
  templateUrl: './user-create-edit.component.html',
  styleUrl: './user-create-edit.component.scss',
  standalone: true
})
export class UserCreateEditComponent extends Base implements OnInit{

  form!: FormGroup;

  @Input() userId?: string;

  constructor(
    private _fb: FormBuilder,
    private _userHttpService: UsersHttpService,
    private _router: Router
  ) {
    super();
  }

  ngOnInit() {
    if (!this.userId) {
      this.buildForm();
    }

    if (this.userId) {
      this.getUser();
    }
  }

  buildForm(userData?: User) {
      this.form = this._fb.group({
        nickname: [userData?.nickname || '', Validators.required],
        email: [userData?.email || '', [Validators.required, Validators.email]],
        first_name: [userData?.first_name || ''],
        surname: [userData?.surname || '']
      }) as FormGroup;
  }

  onCreate(): void {
    if (this.form.valid) {
      const formValue = this.form.getRawValue() as User;
      this._userHttpService.createUser(formValue)
        .pipe(takeUntil(this.destroy$))
        .subscribe(() => {
          this._router.navigate(['/']);
        })
    }
  }

  onUpdate(): void {
    if (this.form.valid) {
      const userId = this.userId as string;
      const formValue = this.form.getRawValue() as User;
      this._userHttpService.patchUser(userId, formValue)
        .pipe(takeUntil(this.destroy$))
        .subscribe(() => {
          this._router.navigate(['/']);
        })
    }
  }

  private getUser() {
    const userId = this.userId as string;
    this._userHttpService.getUser(userId)
        .pipe(takeUntil(this.destroy$))
        .subscribe(res => {
          this.buildForm(res);
        })
  }
}
