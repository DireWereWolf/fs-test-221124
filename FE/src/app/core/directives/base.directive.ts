import {Directive, OnDestroy} from '@angular/core';
import {Subject} from 'rxjs';

@Directive({
  selector: 'bc',
  standalone: true
})
export class Base implements OnDestroy {
  public destroy$: Subject<any> = new Subject();

  ngOnDestroy(): void {
    this.destroy$.next(true);
    this.destroy$.complete();
  }
}
